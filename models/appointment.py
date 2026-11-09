from validation.validation import Validation


class Appointment:
    def __init__(self, appointment_id, customer_id, offering_id, appointment_date, start_time, price_paid, status="pending"):
        self.appointment_id = appointment_id
        self.customer_id = customer_id
        self.offering_id = offering_id
        self.appointment_date = appointment_date
        self.start_time = start_time
        self.price_paid = price_paid
        self.status = status

    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, appointment_id):
        self.__appointment_id = Validation.id_number(appointment_id, "Appointment ID")

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self.__customer_id = Validation.id_number(customer_id, "Customer ID")

    @property
    def offering_id(self):
        return self.__offering_id

    @offering_id.setter
    def offering_id(self, offering_id):
        self.__offering_id = Validation.id_number(offering_id, "Offering ID")

    @property
    def appointment_date(self):
        return self.__appointment_date

    @appointment_date.setter
    def appointment_date(self, appointment_date):
        self.__appointment_date = Validation.appointment_date(appointment_date)

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = Validation.start_time(start_time)

    @property
    def price_paid(self):
        return self.__price_paid

    @price_paid.setter
    def price_paid(self, price_paid):
        self.__price_paid = Validation.money(price_paid, "Price")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = Validation.status(status)

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "customer_id": self.customer_id,
            "offering_id": self.offering_id,
            "appointment_date": str(self.appointment_date),
            "start_time": str(self.start_time),
            "price_paid": str(self.price_paid),
            "status": self.status
        }

    def __repr__(self):
        return f"Appointment(appointment_id={self.appointment_id}, customer_id={self.customer_id}, offering_id={self.offering_id}, appointment_date={self.appointment_date}, start_time={self.start_time}, price_paid={self.price_paid}, status={self.status})"
