import unittest
from datetime import date, time
from decimal import Decimal

from validation.validation import Validation


class TestValidation(unittest.TestCase):
    def test_id_number(self):
        self.assertEqual(Validation.id_number(" 7 ", "Customer ID"), 7)
        for value in (0, -1, "abc", "1.5", True):
            with self.assertRaisesRegex(ValueError, "positive whole number"):
                Validation.id_number(value, "Customer ID")
        for value in ("", "  ", None):
            with self.assertRaisesRegex(ValueError, "Customer ID is required"):
                Validation.id_number(value, "Customer ID")

    def test_name(self):
        self.assertEqual(Validation.name("  Ali Reza ", "Customer name"), "Ali Reza")
        for value in ("ab", "a" * 51, "Ali2", "", None):
            with self.assertRaises(ValueError):
                Validation.name(value, "Customer name")

    def test_money(self):
        self.assertEqual(Validation.money("50", "Price"), Decimal("50.00"))
        self.assertEqual(Validation.money("10.005", "Price"), Decimal("10.01"))
        self.assertEqual(Validation.money(0, "Balance", allow_zero=True), Decimal("0.00"))
        for value in (0, "0.004", -5, "abc", "", "NaN", "1e3", None):
            with self.assertRaisesRegex(ValueError, "greater than zero"):
                Validation.money(value, "Price")
        with self.assertRaisesRegex(ValueError, "zero or more"):
            Validation.money(-1, "Balance", allow_zero=True)

    def test_social_id(self):
        self.assertEqual(Validation.social_id("1234567890"), "1234567890")
        self.assertEqual(Validation.social_id("001-527588-4"), "001-527588-4")
        for value in ("123", "12345678901", "001-527588", ""):
            with self.assertRaises(ValueError):
                Validation.social_id(value)

    def test_age(self):
        self.assertEqual(Validation.age("5"), 5)
        self.assertEqual(Validation.age(80), 80)
        for value in (4, 81, "abc", "", 30.5):
            with self.assertRaises(ValueError):
                Validation.age(value)

    def test_gender(self):
        self.assertEqual(Validation.gender(" Male "), "male")
        with self.assertRaises(ValueError):
            Validation.gender("other")

    def test_phone_number(self):
        self.assertEqual(Validation.phone_number("09123456789"), "09123456789")
        self.assertEqual(Validation.phone_number("+989123456789"), "+989123456789")
        for value in ("0912345678", "08123456789", ""):
            with self.assertRaises(ValueError):
                Validation.phone_number(value)

    def test_offering_type(self):
        self.assertEqual(Validation.offering_type("Facility"), "facility")
        with self.assertRaises(ValueError):
            Validation.offering_type("class")

    def test_duration(self):
        self.assertEqual(Validation.duration("60", "service"), 60)
        self.assertIsNone(Validation.duration("", "facility"))
        self.assertEqual(Validation.duration(90, "facility"), 90)
        with self.assertRaisesRegex(ValueError, "service must have a duration"):
            Validation.duration("", "service")
        for value in (0, -5, "abc", 1.5):
            with self.assertRaises(ValueError):
                Validation.duration(value, "service")

    def test_status(self):
        self.assertEqual(Validation.status("Booked"), "booked")
        with self.assertRaises(ValueError):
            Validation.status("done")

    def test_date_and_time_objects(self):
        self.assertEqual(Validation.appointment_date(date(2030, 1, 5)), date(2030, 1, 5))
        self.assertEqual(Validation.start_time(time(9, 30)), time(9, 30))
        with self.assertRaises(ValueError):
            Validation.appointment_date("2030-01-05")
        with self.assertRaises(ValueError):
            Validation.start_time("09:30")

    def test_date_from_text(self):
        self.assertEqual(Validation.date_from_text("2030-01-05"), date(2030, 1, 5))
        self.assertEqual(Validation.date_from_text("2030-1-5"), date(2030, 1, 5))
        for value in ("05/01/2030", "2030-13-01", "2030-02-30", ""):
            with self.assertRaises(ValueError):
                Validation.date_from_text(value)

    def test_time_from_text(self):
        self.assertEqual(Validation.time_from_text("14:30"), time(14, 30))
        self.assertEqual(Validation.time_from_text("9:05"), time(9, 5))
        for value in ("25:00", "10:60", "2pm", ""):
            with self.assertRaises(ValueError):
                Validation.time_from_text(value)

    def test_center_details(self):
        self.assertEqual(Validation.address(" Main Street "), "Main Street")
        self.assertEqual(Validation.center_phone_number("02166686993"), "02166686993")
        self.assertEqual(Validation.center_phone_number("+982166686993"), "+982166686993")
        for value in ("", "  ", None):
            with self.assertRaises(ValueError):
                Validation.address(value)
        for value in ("0216668699", "2166686993", ""):
            with self.assertRaises(ValueError):
                Validation.center_phone_number(value)


if __name__ == "__main__":
    unittest.main()
