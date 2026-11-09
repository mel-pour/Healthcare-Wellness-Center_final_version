from validation.validation import Validation


class HealthcareCenter:
    def __init__(self, center_id, name, center_address, center_phone_number, offerings=None):
        self.center_id = center_id
        self.name = name
        self.center_address = center_address
        self.center_phone_number = center_phone_number
        if offerings is None:
            self.offerings = []
        else:
            self.offerings = list(offerings)

    @property
    def center_id(self):
        return self.__center_id

    @center_id.setter
    def center_id(self, center_id):
        self.__center_id = Validation.id_number(center_id, "Center ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = Validation.name(name, "Center name")

    @property
    def center_address(self):
        return self.__center_address

    @center_address.setter
    def center_address(self, center_address):
        self.__center_address = Validation.address(center_address)

    @property
    def center_phone_number(self):
        return self.__center_phone_number

    @center_phone_number.setter
    def center_phone_number(self, center_phone_number):
        self.__center_phone_number = Validation.center_phone_number(center_phone_number)

    def to_dict(self):
        return {
            "center_id": self.center_id,
            "name": self.name,
            "center_address": self.center_address,
            "center_phone_number": self.center_phone_number,
            "offering_ids": [offering.offering_id for offering in self.offerings]
        }

    def __repr__(self):
        return f"HealthcareCenter(center_id={self.center_id}, name={self.name}, center_address={self.center_address}, center_phone_number={self.center_phone_number}, offerings={self.offerings})"
