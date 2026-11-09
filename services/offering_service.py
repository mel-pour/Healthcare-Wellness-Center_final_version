from utils.logger import logger


class OfferingService:
    def __init__(self, offering_data_access):
        self.__data_access = offering_data_access

    def save(self, offering):
        if self.__data_access.get_by_id(offering.offering_id) is not None:
            raise ValueError("Offering ID already exists.")
        self.__data_access.save(offering)
        logger.info(f"Offering {offering.offering_id} created")

    def get_by_id(self, offering_id):
        offering = self.__data_access.get_by_id(offering_id)
        if offering is None:
            raise ValueError("Offering not found.")
        return offering

    def get_all(self):
        return self.__data_access.get_all()
