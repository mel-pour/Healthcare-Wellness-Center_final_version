import logging
import unittest
from datetime import date, time
from decimal import Decimal

from data_access.appointment_data_access import AppointmentDataAccess
from data_access.customer_data_access import CustomerDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess
from data_access.offering_data_access import OfferingDataAccess
from models.customer import Customer
from models.healthcare_center import HealthcareCenter
from models.offering import Offering
from services.appointment_service import AppointmentService
from services.customer_service import CustomerService
from services.healthcare_center_service import HealthcareCenterService
from services.offering_service import OfferingService
from test.test_helpers import make_storage

DAY = date(2030, 1, 5)


class TestServices(unittest.TestCase):
    def setUp(self):
        storage = make_storage(self)
        self.customer_data = CustomerDataAccess(storage)
        offering_data = OfferingDataAccess(storage)

        self.customers = CustomerService(self.customer_data)
        self.offerings = OfferingService(offering_data)
        self.appointments = AppointmentService(AppointmentDataAccess(storage), self.customer_data, offering_data)
        self.centers = HealthcareCenterService(HealthcareCenterDataAccess(storage), offering_data)

        self.customers.save(Customer(1, "Milad", "1234567890", 30, "male", "09123456789", 100))
        self.customers.save(Customer(2, "Sara", "1234567891", 25, "female", "09123456788", 100))
        self.offerings.save(Offering(1, "Massage", "service", 50, 60))
        self.offerings.save(Offering(2, "Facial", "service", 40, 30))
        self.offerings.save(Offering(3, "Gym", "facility", 20))

    def balance(self, customer_id):
        return self.customers.get_by_id(customer_id).balance

    # ---------- Customers and offerings ----------

    def test_duplicate_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Customer ID already exists"):
            self.customers.save(Customer(1, "Other", "1234567892", 40, "male", "09123456787", 0))
        with self.assertRaisesRegex(ValueError, "Offering ID already exists"):
            self.offerings.save(Offering(1, "Sauna", "service", 30, 30))

    def test_missing_records_are_reported(self):
        with self.assertRaisesRegex(ValueError, "Customer not found"):
            self.customers.get_by_id(999)
        with self.assertRaisesRegex(ValueError, "Offering not found"):
            self.offerings.get_by_id(999)

    def test_add_balance(self):
        self.customers.add_balance(1, "10.005")
        self.assertEqual(self.balance(1), Decimal("110.01"))
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            self.customers.add_balance(1, "0")
        self.assertEqual(self.balance(1), Decimal("110.01"))

    # ---------- Booking ----------

    def test_booking_charges_the_customer(self):
        self.appointments.book(1, 1, 1, DAY, time(14, 0))
        self.assertEqual(self.appointments.get_by_id(1).status, "booked")
        self.assertEqual(self.appointments.get_by_id(1).price_paid, Decimal("50.00"))
        self.assertEqual(self.balance(1), Decimal("50.00"))

    def test_booking_checks_customer_offering_and_balance(self):
        with self.assertRaisesRegex(ValueError, "Customer not found"):
            self.appointments.book(1, 999, 1, DAY, time(14, 0))
        with self.assertRaisesRegex(ValueError, "Offering not found"):
            self.appointments.book(1, 1, 999, DAY, time(14, 0))

        self.customers.save(Customer(3, "Ali Reza", "1234567892", 40, "male", "09123456787", "49.99"))
        with self.assertRaisesRegex(ValueError, "Insufficient account balance"):
            self.appointments.book(1, 3, 1, DAY, time(14, 0))
        self.assertEqual(self.balance(3), Decimal("49.99"))

    def test_duplicate_appointment_id_charges_nothing(self):
        self.appointments.book(1, 1, 3, DAY, time(9, 0))
        with self.assertRaisesRegex(ValueError, "Appointment ID already exists"):
            self.appointments.book(1, 2, 3, DAY, time(9, 0))
        self.assertEqual(self.balance(2), Decimal("100.00"))

    def test_overlapping_bookings(self):
        self.appointments.book(1, 1, 1, DAY, time(10, 0))

        # Overlap is checked for the whole center, even for another customer and offering.
        with self.assertRaisesRegex(ValueError, "overlaps"):
            self.appointments.book(2, 2, 2, DAY, time(10, 15))
        self.assertEqual(self.balance(2), Decimal("100.00"))

        # Starting when the previous one ends, or on another day, is fine.
        self.appointments.book(3, 2, 2, DAY, time(11, 0))
        self.appointments.book(4, 2, 1, date(2030, 1, 6), time(10, 0))

    def test_cancelled_appointment_does_not_block(self):
        self.appointments.book(1, 1, 1, DAY, time(10, 0))
        self.appointments.cancel(1)
        self.appointments.book(2, 2, 1, DAY, time(10, 0))

    def test_facility_rules(self):
        self.appointments.book(1, 1, 1, DAY, time(10, 0))
        with self.assertRaisesRegex(ValueError, "overlaps"):
            self.appointments.book(2, 2, 3, DAY, time(10, 15))
        self.appointments.book(3, 2, 3, DAY, time(10, 0))
        self.appointments.book(4, 1, 3, DAY, time(12, 0))
        self.appointments.book(5, 2, 3, DAY, time(12, 0))
        self.appointments.book(6, 2, 3, date(2001, 1, 1), time(1, 0))

    # ---------- Cancelling ----------

    def test_cancel_charges_20_percent_fee(self):
        self.appointments.book(1, 1, 1, DAY, time(14, 0))
        self.assertEqual(self.appointments.get_cancellation_details(1),
                         (Decimal("50.00"), Decimal("10.00"), Decimal("40.00")))
        self.assertEqual(self.appointments.get_by_id(1).status, "booked")

        self.assertEqual(self.appointments.cancel(1), (Decimal("10.00"), Decimal("40.00")))
        self.assertEqual(self.appointments.get_by_id(1).status, "cancelled")
        self.assertEqual(self.balance(1), Decimal("90.00"))

    def test_fee_is_rounded(self):
        self.offerings.save(Offering(4, "Sauna", "service", "33.33", 30))
        self.appointments.book(1, 1, 4, DAY, time(14, 0))
        self.assertEqual(self.appointments.get_cancellation_details(1),
                         (Decimal("33.33"), Decimal("6.67"), Decimal("26.66")))

    def test_only_booked_appointments_can_be_cancelled(self):
        self.appointments.book(1, 1, 1, DAY, time(14, 0))
        self.appointments.cancel(1)
        with self.assertRaisesRegex(ValueError, "Only a booked appointment"):
            self.appointments.cancel(1)
        with self.assertRaisesRegex(ValueError, "Appointment not found"):
            self.appointments.cancel(999)
        self.assertEqual(self.balance(1), Decimal("90.00"))

    def test_customer_appointments_and_offering_list(self):
        self.appointments.book(1, 1, 1, DAY, time(14, 0))
        self.assertEqual(len(self.appointments.get_by_customer_id(1)), 1)
        self.assertEqual(len(self.appointments.get_offerings()), 3)
        with self.assertRaisesRegex(ValueError, "Customer not found"):
            self.appointments.get_by_customer_id(999)

    # ---------- Healthcare centers ----------

    def test_center_rules(self):
        self.centers.save(HealthcareCenter(1, "Paradise", "Main Street", "02166686993"))
        with self.assertRaisesRegex(ValueError, "Center ID already exists"):
            self.centers.save(HealthcareCenter(1, "Oasis", "Main Street", "02166686993"))

        self.centers.add_offering(1, 1)
        with self.assertRaisesRegex(ValueError, "already assigned"):
            self.centers.add_offering(1, 1)
        with self.assertRaisesRegex(ValueError, "Offering not found"):
            self.centers.add_offering(1, 999)

        # Editing the details keeps the assigned offerings.
        self.centers.edit(HealthcareCenter(1, "Oasis", "New Street", "02166686994"))
        center = self.centers.get_by_id(1)
        self.assertEqual((center.name, len(center.offerings)), ("Oasis", 1))
        self.assertEqual(len(self.centers.get_all()), 1)

        with self.assertRaisesRegex(ValueError, "center not found"):
            self.centers.get_by_id(999)

    # ---------- Logging ----------

    def test_successful_actions_are_logged(self):
        logging.disable(logging.NOTSET)
        self.addCleanup(logging.disable, logging.CRITICAL)
        with self.assertLogs("healthcare", level="INFO") as logs:
            self.appointments.book(1, 1, 1, DAY, time(14, 0))
            self.appointments.cancel(1)
        self.assertIn("Appointment 1 booked for customer 1", logs.output[0])
        self.assertIn("Appointment 1 cancelled, fee 10.00, refund 40.00", logs.output[1])


if __name__ == "__main__":
    unittest.main()
