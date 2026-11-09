import tkinter as tk
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from controllers.appointment_controller import AppointmentController
from controllers.customer_controller import CustomerController
from controllers.offering_controller import OfferingController
from data_access.appointment_data_access import AppointmentDataAccess
from data_access.customer_data_access import CustomerDataAccess
from data_access.offering_data_access import OfferingDataAccess
from models.customer import Customer
from models.offering import Offering
from services.appointment_service import AppointmentService
from services.customer_service import CustomerService
from services.offering_service import OfferingService
from test.test_helpers import make_storage
from views.appointment_view import AppointmentView
from views.customer_view import CustomerView
from views.main_view import MainView
from views.offering_view import OfferingView


def fill(entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)


class TestViews(unittest.TestCase):
    """Real screens and real layers, with a temporary file. Message boxes are replaced so nothing pops up."""

    def setUp(self):
        storage = make_storage(self)
        self.customer_data = CustomerDataAccess(storage)
        offering_data = OfferingDataAccess(storage)
        self.customer_data.save(Customer(1, "Milad", "1234567890", 30, "male", "09123456789", 100))
        offering_data.save(Offering(1, "Massage", "service", 50, 60))
        offering_data.save(Offering(2, "Gym", "facility", 20))

        self.customer_controller = CustomerController(CustomerService(self.customer_data))
        self.offering_controller = OfferingController(OfferingService(offering_data))
        self.appointment_controller = AppointmentController(
            AppointmentService(AppointmentDataAccess(storage), self.customer_data, offering_data))

        self.root = tk.Tk()
        self.addCleanup(self.root.destroy)

        self.showinfo = patch("tkinter.messagebox.showinfo").start()
        self.showerror = patch("tkinter.messagebox.showerror").start()
        self.askyesno = patch("tkinter.messagebox.askyesno").start()
        self.addCleanup(patch.stopall)

    def last_error(self):
        return self.showerror.call_args[0][1]

    def balance(self):
        return self.customer_data.get_by_id(1).balance

    def test_main_menu_opens_every_screen(self):
        main_view = MainView(self.root, self.customer_controller, self.appointment_controller, self.offering_controller)
        main_view.open_customer_view()
        main_view.open_appointment_view()
        main_view.open_offering_view()
        main_view.show_main_menu()
        self.showerror.assert_not_called()

    def test_customer_search(self):
        view = CustomerView(self.root, self.customer_controller, None)
        fill(view.customer_id_entry, "1")
        view.search_customer()
        self.assertEqual(view.name_label["text"], "Milad")

        fill(view.customer_id_entry, "999")
        view.search_customer()
        self.assertEqual(self.last_error(), "Error : Customer not found.")
        self.assertEqual(view.name_label["text"], "-")

    def test_add_balance_needs_a_customer_first(self):
        view = CustomerView(self.root, self.customer_controller, None)
        view.show_balance_form()
        self.assertEqual(self.last_error(), "Error : Customer ID is required.")

    def test_create_offering(self):
        view = OfferingView(self.root, self.offering_controller, None)
        self.assertEqual(view.offerings_list.get(1), "ID: 2 | Gym | Type: facility | Price: $20.00 | Duration: N/A")

        fill(view.id_entry, "3")
        fill(view.name_entry, "Sauna")
        fill(view.price_entry, "30")
        fill(view.duration_entry, "45")
        view.save_click()
        self.assertEqual(view.offerings_list.size(), 3)

        fill(view.id_entry, "3")
        view.save_click()
        self.assertEqual(self.last_error(), "Error : Offering name must be 3 to 50 letters or spaces.")

    def test_book_and_cancel(self):
        view = AppointmentView(self.root, self.appointment_controller, None)
        fill(view.customer_id_entry, "1")
        fill(view.appointment_id_entry, "1")
        view.offering_combo.current(0)
        fill(view.date_entry, "2030-01-05")
        fill(view.time_entry, "14:30")
        view.book_click()
        self.showerror.assert_not_called()
        self.assertEqual(self.balance(), Decimal("50.00"))
        self.assertIn("Status: booked", view.results.get("1.0", tk.END))

        # Answering "No" changes nothing.
        fill(view.appointment_id_entry, "1")
        self.askyesno.return_value = False
        view.cancel_click()
        self.assertEqual(self.balance(), Decimal("50.00"))

        # Answering "Yes" cancels and refunds 80%.
        self.askyesno.return_value = True
        view.cancel_click()
        self.assertIn("Cancellation fee: $10.00", self.askyesno.call_args[0][1])
        self.assertEqual(self.balance(), Decimal("90.00"))
        self.assertIn("Status: cancelled", view.results.get("1.0", tk.END))

    def test_booking_without_an_offering(self):
        view = AppointmentView(self.root, self.appointment_controller, None)
        view.offering_combo.set("")
        fill(view.customer_id_entry, "1")
        fill(view.appointment_id_entry, "1")
        view.book_click()
        self.assertEqual(self.last_error(), "Error : Offering ID is required.")

    def test_views_only_talk_to_controllers(self):
        folder = Path(__file__).resolve().parent.parent / "views"
        for path in folder.glob("*_view.py"):
            source = path.read_text(encoding="utf-8")
            for forbidden in ("try:", "services", "data_access", "models", "validation", "open("):
                self.assertNotIn(forbidden, source, f"{path.name} contains {forbidden}")


if __name__ == "__main__":
    unittest.main()
