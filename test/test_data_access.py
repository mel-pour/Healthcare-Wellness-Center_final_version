import unittest
from datetime import date, time
from decimal import Decimal
from pathlib import Path

from data_access.appointment_data_access import AppointmentDataAccess
from data_access.customer_data_access import CustomerDataAccess
from data_access.healthcare_center_data_access import HealthcareCenterDataAccess
from data_access.offering_data_access import OfferingDataAccess
from data_access.text_file_storage import TextFileStorage
from models.appointment import Appointment
from models.customer import Customer
from models.healthcare_center import HealthcareCenter
from models.offering import Offering
from test.test_helpers import make_storage


class TestDataAccess(unittest.TestCase):
    def setUp(self):
        self.storage = make_storage(self)
        self.customers = CustomerDataAccess(self.storage)
        self.offerings = OfferingDataAccess(self.storage)
        self.appointments = AppointmentDataAccess(self.storage)
        self.centers = HealthcareCenterDataAccess(self.storage)

    def test_storage_saves_and_loads(self):
        data = {"customers": [{"name": "میلاد"}], "offerings": [], "appointments": [], "centers": []}
        self.storage.save(data)
        self.assertEqual(self.storage.load(), data)

    def test_default_storage_points_to_the_real_file(self):
        # Only builds the object. It never opens the real file.
        path = Path(TextFileStorage().file_path)
        self.assertEqual((path.parent.name, path.name), ("data", "healthcare_data.txt"))

    def test_customer_save_get_and_edit(self):
        customer = Customer(1, "Milad", "1234567890", 30, "male", "09123456789", 100)
        self.customers.save(customer)
        self.assertEqual(self.customers.get_by_id(1).name, "Milad")
        self.assertIsNone(self.customers.get_by_id(999))

        customer.balance = 40
        self.customers.edit(customer)
        self.assertEqual(self.customers.get_by_id(1).balance, Decimal("40.00"))
        self.assertEqual(len(self.customers.get_all()), 1)

    def test_offering_save_and_get(self):
        self.offerings.save(Offering(1, "Massage", "service", 50, 60))
        self.offerings.save(Offering(2, "Gym", "facility", 20))
        self.assertEqual(self.offerings.get_by_id(1).duration, 60)
        self.assertIsNone(self.offerings.get_by_id(2).duration)
        self.assertEqual(len(self.offerings.get_all()), 2)

    def test_appointment_save_get_and_edit(self):
        appointment = Appointment(1, 10, 20, date(2030, 1, 5), time(14, 30), 50, "booked")
        self.appointments.save(appointment)
        self.appointments.save(Appointment(2, 11, 20, date(2030, 1, 5), time(16, 0), 50, "booked"))

        found = self.appointments.get_by_id(1)
        self.assertEqual((found.appointment_date, found.start_time), (date(2030, 1, 5), time(14, 30)))
        self.assertEqual(len(self.appointments.get_by_customer_id(10)), 1)

        appointment.status = "cancelled"
        self.appointments.edit(appointment)
        self.assertEqual(self.appointments.get_by_id(1).status, "cancelled")

    def test_center_offerings_are_rebuilt_from_ids(self):
        massage = Offering(5, "Massage", "service", 50, 60)
        self.offerings.save(massage)
        self.offerings.save(Offering(6, "Gym", "facility", 20))
        self.centers.save(HealthcareCenter(1, "Paradise", "Main Street", "02166686993", [massage]))

        center = self.centers.get_by_id(1)
        self.assertEqual([offering.name for offering in center.offerings], ["Massage"])

    def test_all_classes_share_one_file(self):
        self.customers.save(Customer(1, "Milad", "1234567890", 30, "male", "09123456789", 100))
        self.offerings.save(Offering(1, "Massage", "service", 50, 60))
        self.appointments.save(Appointment(1, 1, 1, date(2030, 1, 5), time(14, 30), 50, "booked"))
        self.centers.save(HealthcareCenter(1, "Paradise", "Main Street", "02166686993"))

        for data_access in (self.customers, self.offerings, self.appointments, self.centers):
            self.assertEqual(len(data_access.get_all()), 1)


if __name__ == "__main__":
    unittest.main()
