from models.offering import Offering


class OfferingDataAccess:
    def __init__(self, storage):
        self.__storage = storage

    def save(self, offering):
        data = self.__storage.load()
        data["offerings"].append(offering.to_dict())
        self.__storage.save(data)

    def edit(self, offering):
        data = self.__storage.load()
        for index, item in enumerate(data["offerings"]):
            if item["offering_id"] == offering.offering_id:
                data["offerings"][index] = offering.to_dict()
        self.__storage.save(data)

    def get_all(self):
        data = self.__storage.load()
        offering_list = []
        for item in data["offerings"]:
            offering_list.append(Offering(item["offering_id"], item["name"], item["offering_type"],
                                          item["price"], item["duration"]))
        return offering_list

    def get_by_id(self, offering_id):
        for offering in self.get_all():
            if offering.offering_id == offering_id:
                return offering
        return None
