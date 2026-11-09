from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from models.appointment import Appointment
from utils.logger import logger


class AppointmentService:
    def __init__(self, appointment_data_access, customer_data_access, offering_data_access):
        self.__appointment_data_access = appointment_data_access
        self.__customer_data_access = customer_data_access
        self.__offering_data_access = offering_data_access

    def book(self, appointment_id, customer_id, offering_id, appointment_date, start_time):
        customer = self.get_customer(customer_id)
        offering = self.__get_offering(offering_id)

        if customer.balance < offering.price:
            raise ValueError("Insufficient account balance.")

        self.__check_overlap(offering, appointment_date, start_time)

        appointment = Appointment(appointment_id, customer_id, offering_id, appointment_date,
                                  start_time, offering.price, "booked")

        if self.__appointment_data_access.get_by_id(appointment.appointment_id) is not None:
            raise ValueError("Appointment ID already exists.")

        self.__appointment_data_access.save(appointment)

        customer.balance = customer.balance - offering.price
        self.__customer_data_access.edit(customer)
        logger.info(f"Appointment {appointment_id} booked for customer {customer_id}")

    def cancel(self, appointment_id):
        price, fee, refund = self.get_cancellation_details(appointment_id)
        appointment = self.get_by_id(appointment_id)
        customer = self.get_customer(appointment.customer_id)

        appointment.status = "cancelled"
        self.__appointment_data_access.edit(appointment)

        customer.balance = customer.balance + refund
        self.__customer_data_access.edit(customer)
        logger.info(f"Appointment {appointment_id} cancelled, fee {fee}, refund {refund}")

        return fee, refund

    def get_cancellation_details(self, appointment_id):
        appointment = self.get_by_id(appointment_id)

        if appointment.status != "booked":
            raise ValueError("Only a booked appointment can be cancelled.")

        price = appointment.price_paid
        fee = (price * Decimal("0.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return price, fee, price - fee

    def get_by_id(self, appointment_id):
        appointment = self.__appointment_data_access.get_by_id(appointment_id)
        if appointment is None:
            raise ValueError("Appointment not found.")
        return appointment

    def get_by_customer_id(self, customer_id):
        self.get_customer(customer_id)
        return self.__appointment_data_access.get_by_customer_id(customer_id)

    def get_customer(self, customer_id):
        customer = self.__customer_data_access.get_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")
        return customer

    def get_offerings(self):
        return self.__offering_data_access.get_all()

    def __get_offering(self, offering_id):
        offering = self.__offering_data_access.get_by_id(offering_id)
        if offering is None:
            raise ValueError("Offering not found.")
        return offering

    def __check_overlap(self, offering, appointment_date, start_time):
        new_start = datetime.combine(appointment_date, start_time)
        new_end = new_start + timedelta(minutes=offering.duration or 0)

        for existing in self.__appointment_data_access.get_all():
            if existing.status == "booked" and existing.appointment_date == appointment_date:
                existing_offering = self.__get_offering(existing.offering_id)
                existing_start = datetime.combine(existing.appointment_date, existing.start_time)
                existing_end = existing_start + timedelta(minutes=existing_offering.duration or 0)

                if new_start < existing_end and existing_start < new_end:
                    raise ValueError("This appointment overlaps with an existing booking.")
