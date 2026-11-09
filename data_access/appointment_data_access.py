from datetime import date, time

from models.appointment import Appointment


class AppointmentDataAccess:
    def __init__(self, storage):
        self.__storage = storage

    def save(self, appointment):
        data = self.__storage.load()
        data["appointments"].append(appointment.to_dict())
        self.__storage.save(data)

    def edit(self, appointment):
        data = self.__storage.load()
        for index, item in enumerate(data["appointments"]):
            if item["appointment_id"] == appointment.appointment_id:
                data["appointments"][index] = appointment.to_dict()
        self.__storage.save(data)

    def get_all(self):
        data = self.__storage.load()
        appointment_list = []
        for item in data["appointments"]:
            appointment_list.append(Appointment(item["appointment_id"], item["customer_id"], item["offering_id"],
                                                date.fromisoformat(item["appointment_date"]),
                                                time.fromisoformat(item["start_time"]),
                                                item["price_paid"], item["status"]))
        return appointment_list

    def get_by_id(self, appointment_id):
        for appointment in self.get_all():
            if appointment.appointment_id == appointment_id:
                return appointment
        return None

    def get_by_customer_id(self, customer_id):
        appointment_list = []
        for appointment in self.get_all():
            if appointment.customer_id == customer_id:
                appointment_list.append(appointment)
        return appointment_list
