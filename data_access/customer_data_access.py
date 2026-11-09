from models.customer import Customer


class CustomerDataAccess:
    def __init__(self, storage):
        self.__storage = storage

    def save(self, customer):
        data = self.__storage.load()
        data["customers"].append(customer.to_dict())
        self.__storage.save(data)

    def edit(self, customer):
        data = self.__storage.load()
        for index, item in enumerate(data["customers"]):
            if item["customer_id"] == customer.customer_id:
                data["customers"][index] = customer.to_dict()
        self.__storage.save(data)

    def get_all(self):
        data = self.__storage.load()
        customer_list = []
        for item in data["customers"]:
            customer_list.append(Customer(item["customer_id"], item["name"], item["social_id"], item["age"],
                                          item["gender"], item["phone_number"], item["balance"]))
        return customer_list

    def get_by_id(self, customer_id):
        for customer in self.get_all():
            if customer.customer_id == customer_id:
                return customer
        return None
