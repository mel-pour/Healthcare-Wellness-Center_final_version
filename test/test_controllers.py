import logging
import os
import unittest
from decimal import Decimal

from controllers.appointment_controller import AppointmentController
from controllers.customer_controller import CustomerController
from controllers.healthcare_center_controller import HealthcareCenterController
from controllers.offering_controller import OfferingController
from data_access.appointment_data_access import AppointmentDataAccess
from data_access.customer_data_access import CustomerDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess
from data_access.offering_data_access import OfferingDataAccess
from services.appointment_service import AppointmentService
from services.customer_service import CustomerService
from services.healthcare_center_service import HealthcareCenterService
from services.offering_service import OfferingService
from test.test_helpers import make_storage


class TestControllers(unittest.TestCase):
    """Sends text like a screen would, through every layer, down to a temporary file."""

    def setUp(self):
        self.storage = make_storage(self)
        customer_data = CustomerDataAccess(self.storage)
        offering_data = OfferingDataAccess(self.storage)

        self.customer = CustomerController(CustomerService(customer_data))
        self.offering = OfferingController(OfferingService(offering_data))
        self.appointment = AppointmentController(
            AppointmentService(AppointmentDataAccess(self.storage), customer_data, offering_data))
        self.center = HealthcareCenterController(
            HealthcareCenterService(HealthcareCenterDataAccess(self.storage), offering_data))

        self.customer.save("1", "Milad", "1234567890", "30", "male", "09123456789", "100")
        self.offering.save("1", "Massage", "service", "50", "60")

    def test_customer_flow(self):
        self.assertEqual(self.customer.save("2", "Sara", "1234567891", "25", "female", "09123456788", "0"),
                         (True, "Info : Customer Sara Saved"))
        self.assertEqual(self.customer.add_balance("1", "25.50"), (True, "Info : Balance Added to Customer 1"))

        success, customer = self.customer.get_by_id(" 1 ")
        self.assertTrue(success)
        self.assertEqual(customer.balance, Decimal("125.50"))

    def test_validation_errors_become_messages(self):
        self.assertEqual(self.customer.save("3", "Ali", "1234567892", "abc", "male", "09123456787", "0"),
                         (False, "Error : Age must be a whole number between 5 and 80."))
        self.assertEqual(self.customer.get_by_id("abc"),
                         (False, "Error : Customer ID must be a positive whole number."))
        self.assertEqual(self.customer.add_balance(None, "10"), (False, "Error : Customer ID is required."))
        self.assertEqual(self.offering.save("2", "Sauna", "service", "30", ""),
                         (False, "Error : A service must have a duration."))
        self.assertEqual(self.appointment.book("1", "1", "", "2030-01-05", "14:30"),
                         (False, "Error : Offering ID is required."))
        self.assertEqual(self.appointment.book("1", "1", "1", "05/01/2030", "14:30"),
                         (False, "Error : Please enter a valid date in YYYY-MM-DD format."))
        self.assertEqual(self.appointment.book("1", "1", "1", "2030-01-05", "2pm"),
                         (False, "Error : Please enter a valid time in HH:MM format, using 24-hour time."))

    def test_business_rule_errors_become_messages(self):
        self.assertEqual(self.customer.save("1", "Copy", "1234567892", "40", "male", "09123456787", "0"),
                         (False, "Error : Customer ID already exists."))
        self.assertEqual(self.customer.get_by_id("999"), (False, "Error : Customer not found."))
        self.offering.save("2", "Facial", "service", "500", "30")
        self.assertEqual(self.appointment.book("1", "1", "2", "2030-01-05", "14:30"),
                         (False, "Error : Insufficient account balance."))

    def test_unexpected_errors_become_messages(self):
        os.remove(self.storage.file_path)
        success, message = self.customer.get_by_id("1")
        self.assertFalse(success)
        self.assertIn("No such file", message)

    def test_booking_and_cancelling(self):
        self.assertEqual(self.appointment.book("1", "1", "1", "2030-01-05", "14:30"),
                         (True, "Info : Appointment 1 Booked"))
        self.assertEqual(self.appointment.get_customer("1")[1].balance, Decimal("50.00"))
        self.assertEqual(len(self.appointment.get_by_customer_id("1")[1]), 1)
        self.assertEqual(len(self.appointment.get_offerings()[1]), 1)
        self.assertEqual(self.appointment.get_cancellation_details("1"),
                         (True, (Decimal("50.00"), Decimal("10.00"), Decimal("40.00"))))

        self.assertEqual(self.appointment.cancel("1"),
                         (True, "Info : Appointment 1 Cancelled\nCancellation fee: $10.00\nRefund: $40.00"))
        self.assertEqual(self.appointment.get_by_id("1")[1].status, "cancelled")
        self.assertEqual(self.appointment.cancel("1"),
                         (False, "Error : Only a booked appointment can be cancelled."))

    def test_offering_flow(self):
        self.assertEqual(self.offering.save("2", "Gym", "facility", "20", ""), (True, "Info : Offering Gym Saved"))
        self.assertEqual(self.offering.get_by_id("2")[1].name, "Gym")
        self.assertEqual(len(self.offering.get_all()[1]), 2)

    def test_center_flow(self):
        self.assertEqual(self.center.save("1", "Paradise", "Main Street", "02166686993"),
                         (True, "Info : Center Paradise Saved"))
        self.assertEqual(self.center.add_offering("1", "1"), (True, "Info : Offering 1 Added to Center 1"))
        self.assertEqual(self.center.edit("1", "Oasis", "Main Street", "02166686993"),
                         (True, "Info : Center Oasis Edited"))
        self.assertEqual(len(self.center.get_by_id("1")[1].offerings), 1)
        self.assertEqual(len(self.center.get_all()[1]), 1)

    def test_errors_are_logged(self):
        logging.disable(logging.NOTSET)
        self.addCleanup(logging.disable, logging.CRITICAL)

        with self.assertLogs("healthcare", level="WARNING") as logs:
            self.customer.get_by_id("999")
        self.assertIn("WARNING", logs.output[0])
        self.assertIn("CustomerController.get_by_id: Customer not found.", logs.output[0])

        os.remove(self.storage.file_path)
        with self.assertLogs("healthcare", level="ERROR") as logs:
            self.customer.get_by_id("1")
        self.assertIn("Unexpected error in CustomerController.get_by_id", logs.output[0])
        self.assertIn("Traceback", logs.output[0])


if __name__ == "__main__":
    unittest.main()
