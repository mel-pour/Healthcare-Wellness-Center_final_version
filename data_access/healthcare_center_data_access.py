from models.healthcare_center import HealthcareCenter
from models.offering import Offering


class HealthcareCenterDataAccess:
    def __init__(self, storage):
        self.__storage = storage

    def save(self, center):
        data = self.__storage.load()
        data["centers"].append(center.to_dict())
        self.__storage.save(data)

    def edit(self, center):
        data = self.__storage.load()
        for index, item in enumerate(data["centers"]):
            if item["center_id"] == center.center_id:
                data["centers"][index] = center.to_dict()
        self.__storage.save(data)

    def get_all(self):
        data = self.__storage.load()
        center_list = []
        for item in data["centers"]:
            # The file keeps only offering ids, so rebuild the offering objects.
            offerings = []
            for offering in data["offerings"]:
                if offering["offering_id"] in item["offering_ids"]:
                    offerings.append(Offering(offering["offering_id"], offering["name"], offering["offering_type"],
                                              offering["price"], offering["duration"]))
            center_list.append(HealthcareCenter(item["center_id"], item["name"], item["center_address"],
                                                item["center_phone_number"], offerings))
        return center_list

    def get_by_id(self, center_id):
        for center in self.get_all():
            if center.center_id == center_id:
                return center
        return None
