from controllers.error_handler import handle_errors
from validation.validation import Validation


class AppointmentController:
    def __init__(self, appointment_service):
        self.__service = appointment_service

    @handle_errors
    def book(self, appointment_id, customer_id, offering_id, appointment_date, start_time):
        appointment_id = Validation.id_number(appointment_id, "Appointment ID")
        customer_id = Validation.id_number(customer_id, "Customer ID")
        offering_id = Validation.id_number(offering_id, "Offering ID")
        appointment_date = Validation.date_from_text(appointment_date)
        start_time = Validation.time_from_text(start_time)
        self.__service.book(appointment_id, customer_id, offering_id, appointment_date, start_time)
        return True, f"Info : Appointment {appointment_id} Booked"

    @handle_errors
    def cancel(self, appointment_id):
        appointment_id = Validation.id_number(appointment_id, "Appointment ID")
        fee, refund = self.__service.cancel(appointment_id)
        return True, f"Info : Appointment {appointment_id} Cancelled\nCancellation fee: ${fee}\nRefund: ${refund}"

    @handle_errors
    def get_cancellation_details(self, appointment_id):
        details = self.__service.get_cancellation_details(Validation.id_number(appointment_id, "Appointment ID"))
        return True, details

    @handle_errors
    def get_by_id(self, appointment_id):
        appointment = self.__service.get_by_id(Validation.id_number(appointment_id, "Appointment ID"))
        return True, appointment

    @handle_errors
    def get_by_customer_id(self, customer_id):
        appointments = self.__service.get_by_customer_id(Validation.id_number(customer_id, "Customer ID"))
        return True, appointments

    @handle_errors
    def get_customer(self, customer_id):
        customer = self.__service.get_customer(Validation.id_number(customer_id, "Customer ID"))
        return True, customer

    @handle_errors
    def get_offerings(self):
        offerings = self.__service.get_offerings()
        return True, offerings
