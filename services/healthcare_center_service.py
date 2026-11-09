from utils.logger import logger


class HealthcareCenterService:
    def __init__(self, center_data_access, offering_data_access):
        self.__center_data_access = center_data_access
        self.__offering_data_access = offering_data_access

    def save(self, center):
        if self.__center_data_access.get_by_id(center.center_id) is not None:
            raise ValueError("Center ID already exists.")
        self.__center_data_access.save(center)
        logger.info(f"Center {center.center_id} created")

    def edit(self, center):
        # Editing the details must not lose the offerings already assigned.
        center.offerings = self.get_by_id(center.center_id).offerings
        self.__center_data_access.edit(center)
        logger.info(f"Center {center.center_id} edited")

    def get_by_id(self, center_id):
        center = self.__center_data_access.get_by_id(center_id)
        if center is None:
            raise ValueError("Healthcare center not found.")
        return center

    def get_all(self):
        return self.__center_data_access.get_all()

    def add_offering(self, center_id, offering_id):
        center = self.get_by_id(center_id)
        offering = self.__offering_data_access.get_by_id(offering_id)

        if offering is None:
            raise ValueError("Offering not found.")

        for existing in center.offerings:
            if existing.offering_id == offering_id:
                raise ValueError("This offering is already assigned to the center.")

        center.offerings.append(offering)
        self.__center_data_access.edit(center)
        logger.info(f"Offering {offering_id} added to center {center_id}")
