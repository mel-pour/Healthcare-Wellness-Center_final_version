import re
from datetime import date, time
from decimal import Decimal, ROUND_HALF_UP


class Validation:
    """All input checks live here. Each method returns the clean value or raises ValueError."""

    # ---------- Shared ----------

    @staticmethod
    def id_number(value, field_name):
        text = "" if value is None else str(value).strip()
        if text == "":
            raise ValueError(f"{field_name} is required.")
        if not text.isdecimal() or int(text) <= 0:
            raise ValueError(f"{field_name} must be a positive whole number.")
        return int(text)

    @staticmethod
    def name(value, field_name):
        if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z\s]{3,50}", value.strip()):
            raise ValueError(f"{field_name} must be 3 to 50 letters or spaces.")
        return value.strip()

    @staticmethod
    def money(value, field_name, allow_zero=False):
        if allow_zero:
            message = f"{field_name} must be a number that is zero or more."
        else:
            message = f"{field_name} must be a number greater than zero."

        text = str(value).strip()
        if not re.fullmatch(r"\d+(\.\d+)?", text):
            raise ValueError(message)

        amount = Decimal(text).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if amount == 0 and not allow_zero:
            raise ValueError(message)
        return amount

    # ---------- Customer ----------

    @staticmethod
    def social_id(value):
        text = str(value).strip()
        if not re.fullmatch(r"\d{10}|\d{3}-\d{6}-\d", text):
            raise ValueError("Social ID must be 10 digits or in the format 123-456789-0.")
        return text

    @staticmethod
    def age(value):
        text = str(value).strip()
        if not text.isdecimal() or not 5 <= int(text) <= 80:
            raise ValueError("Age must be a whole number between 5 and 80.")
        return int(text)

    @staticmethod
    def gender(value):
        text = str(value).strip().lower()
        if text not in ("male", "female"):
            raise ValueError("Gender must be male or female.")
        return text

    @staticmethod
    def phone_number(value):
        text = str(value).strip()
        if not re.fullmatch(r"09\d{9}|\+989\d{9}", text):
            raise ValueError("Phone number must look like 09123456789 or +989123456789.")
        return text

    # ---------- Offering ----------

    @staticmethod
    def offering_type(value):
        text = str(value).strip().lower()
        if text not in ("service", "facility"):
            raise ValueError("Offering type must be service or facility.")
        return text

    @staticmethod
    def duration(value, offering_type):
        # An empty entry box means "no duration".
        if value is None or str(value).strip() == "":
            if offering_type == "service":
                raise ValueError("A service must have a duration.")
            return None

        text = str(value).strip()
        if not text.isdecimal() or int(text) <= 0:
            raise ValueError("Duration must be a positive whole number of minutes.")
        return int(text)

    # ---------- Appointment ----------

    @staticmethod
    def appointment_date(value):
        if not isinstance(value, date):
            raise ValueError("Appointment date must be a valid date.")
        return value

    @staticmethod
    def start_time(value):
        if not isinstance(value, time):
            raise ValueError("Start time must be a valid time.")
        return value

    @staticmethod
    def status(value):
        text = str(value).strip().lower()
        if text not in ("pending", "booked", "cancelled"):
            raise ValueError("Status must be pending, booked, or cancelled.")
        return text

    @staticmethod
    def date_from_text(value):
        text = str(value).strip()
        if not re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", text):
            raise ValueError("Please enter a valid date in YYYY-MM-DD format.")
        year, month, day = text.split("-")
        return date(int(year), int(month), int(day))

    @staticmethod
    def time_from_text(value):
        text = str(value).strip()
        if not re.fullmatch(r"\d{1,2}:\d{1,2}", text):
            raise ValueError("Please enter a valid time in HH:MM format, using 24-hour time.")
        hour, minute = text.split(":")
        return time(int(hour), int(minute))

    # ---------- Healthcare center ----------

    @staticmethod
    def address(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address cannot be empty.")
        return value.strip()

    @staticmethod
    def center_phone_number(value):
        text = str(value).strip()
        if not re.fullmatch(r"0\d{10}|\+98\d{10}", text):
            raise ValueError("Center phone number must look like 02166686993 or +982166686993.")
        return text
