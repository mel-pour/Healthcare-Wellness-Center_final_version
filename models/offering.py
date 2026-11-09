from validation.validation import Validation


class Offering:
    def __init__(self, offering_id, name, offering_type, price, duration=None):
        self.offering_id = offering_id
        self.name = name
        self.offering_type = offering_type
        self.price = price
        self.duration = duration

    @property
    def offering_id(self):
        return self.__offering_id

    @offering_id.setter
    def offering_id(self, offering_id):
        self.__offering_id = Validation.id_number(offering_id, "Offering ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = Validation.name(name, "Offering name")

    @property
    def offering_type(self):
        return self.__offering_type

    @offering_type.setter
    def offering_type(self, offering_type):
        self.__offering_type = Validation.offering_type(offering_type)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = Validation.money(price, "Price")

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = Validation.duration(duration, self.offering_type)

    def to_dict(self):
        return {
            "offering_id": self.offering_id,
            "name": self.name,
            "offering_type": self.offering_type,
            "price": str(self.price),
            "duration": self.duration
        }

    def __repr__(self):
        return f"Offering(offering_id={self.offering_id}, name={self.name}, offering_type={self.offering_type}, price={self.price}, duration={self.duration})"
