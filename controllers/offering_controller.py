from controllers.error_handler import handle_errors
from models.offering import Offering
from validation.validation import Validation


class OfferingController:
    def __init__(self, offering_service):
        self.__service = offering_service

    @handle_errors
    def save(self, offering_id, name, offering_type, price, duration=None):
        offering = Offering(offering_id, name, offering_type, price, duration)
        self.__service.save(offering)
        return True, f"Info : Offering {offering.name} Saved"

    @handle_errors
    def get_by_id(self, offering_id):
        offering = self.__service.get_by_id(Validation.id_number(offering_id, "Offering ID"))
        return True, offering

    @handle_errors
    def get_all(self):
        offerings = self.__service.get_all()
        return True, offerings
