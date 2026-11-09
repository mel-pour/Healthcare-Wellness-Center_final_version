import unittest
from datetime import date, time
from decimal import Decimal

from models.appointment import Appointment
from models.customer import Customer
from models.healthcare_center import HealthcareCenter
from models.offering import Offering


class TestModels(unittest.TestCase):
    def test_customer_converts_text_from_the_screen(self):
        customer = Customer("1", "Milad", "1234567890", "30", "Male", "09123456789", "100")
        self.assertEqual(customer.customer_id, 1)
        self.assertEqual(customer.age, 30)
        self.assertEqual(customer.gender, "male")
        self.assertEqual(customer.balance, Decimal("100.00"))

    def test_setter_runs_on_every_change(self):
        customer = Customer(1, "Milad", "1234567890", 30, "male", "09123456789", 100)
        with self.assertRaises(ValueError):
            customer.age = 200
        self.assertEqual(customer.age, 30)

    def test_invalid_values_are_rejected(self):
        with self.assertRaises(ValueError):
            Customer(1, "Milad", "123", 30, "male", "09123456789", 100)
        with self.assertRaises(ValueError):
            Offering(1, "Massage", "service", 50)
        with self.assertRaises(ValueError):
            Appointment(1, 2, 3, "2030-01-05", time(14, 30), 50)
        with self.assertRaises(ValueError):
            HealthcareCenter(1, "Paradise", "", "02166686993")

    def test_facility_does_not_need_duration(self):
        self.assertIsNone(Offering(2, "Gym", "facility", 20, "").duration)

    def test_appointment_status(self):
        appointment = Appointment(1, 2, 3, date(2030, 1, 5), time(14, 30), 50)
        self.assertEqual(appointment.status, "pending")
        appointment.status = "Cancelled"
        self.assertEqual(appointment.status, "cancelled")

    def test_centers_do_not_share_offerings(self):
        first = HealthcareCenter(1, "Paradise", "Main Street", "02166686993")
        second = HealthcareCenter(2, "Oasis", "Main Street", "02166686993")
        first.offerings.append(Offering(1, "Massage", "service", 50, 60))
        self.assertEqual(second.offerings, [])

    def test_to_dict_matches_the_data_file(self):
        self.assertEqual(Customer(1, "Milad", "1234567890", 30, "male", "09123456789", 100).to_dict(),
                         {"customer_id": 1, "name": "Milad", "social_id": "1234567890", "age": 30,
                          "gender": "male", "phone_number": "09123456789", "balance": "100.00"})
        self.assertEqual(Offering(2, "Gym", "facility", 20).to_dict(),
                         {"offering_id": 2, "name": "Gym", "offering_type": "facility",
                          "price": "20.00", "duration": None})
        self.assertEqual(Appointment(1, 2, 3, date(2030, 1, 5), time(14, 30), 50, "booked").to_dict(),
                         {"appointment_id": 1, "customer_id": 2, "offering_id": 3, "appointment_date": "2030-01-05",
                          "start_time": "14:30:00", "price_paid": "50.00", "status": "booked"})
        center = HealthcareCenter(1, "Paradise", "Main Street", "02166686993",
                                  [Offering(5, "Massage", "service", 50, 60)])
        self.assertEqual(center.to_dict()["offering_ids"], [5])


if __name__ == "__main__":
    unittest.main()
