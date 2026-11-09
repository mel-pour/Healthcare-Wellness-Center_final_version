from controllers.error_handler import handle_errors
from models.healthcare_center import HealthcareCenter
from validation.validation import Validation


class HealthcareCenterController:
    def __init__(self, center_service):
        self.__service = center_service

    @handle_errors
    def save(self, center_id, name, center_address, center_phone_number):
        center = HealthcareCenter(center_id, name, center_address, center_phone_number)
        self.__service.save(center)
        return True, f"Info : Center {center.name} Saved"

    @handle_errors
    def edit(self, center_id, name, center_address, center_phone_number):
        center = HealthcareCenter(center_id, name, center_address, center_phone_number)
        self.__service.edit(center)
        return True, f"Info : Center {center.name} Edited"

    @handle_errors
    def get_by_id(self, center_id):
        center = self.__service.get_by_id(Validation.id_number(center_id, "Center ID"))
        return True, center

    @handle_errors
    def get_all(self):
        centers = self.__service.get_all()
        return True, centers

    @handle_errors
    def add_offering(self, center_id, offering_id):
        center_id = Validation.id_number(center_id, "Center ID")
        offering_id = Validation.id_number(offering_id, "Offering ID")
        self.__service.add_offering(center_id, offering_id)
        return True, f"Info : Offering {offering_id} Added to Center {center_id}"
