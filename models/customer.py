from validation.validation import Validation


class Customer:
    def __init__(self, customer_id, name, social_id, age, gender, phone_number, balance):
        self.customer_id = customer_id
        self.name = name
        self.social_id = social_id
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.balance = balance

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self.__customer_id = Validation.id_number(customer_id, "Customer ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = Validation.name(name, "Customer name")

    @property
    def social_id(self):
        return self.__social_id

    @social_id.setter
    def social_id(self, social_id):
        self.__social_id = Validation.social_id(social_id)

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = Validation.age(age)

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        self.__gender = Validation.gender(gender)

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self.__phone_number = Validation.phone_number(phone_number)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance):
        self.__balance = Validation.money(balance, "Balance", allow_zero=True)

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "social_id": self.social_id,
            "age": self.age,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "balance": str(self.balance)
        }

    def __repr__(self):
        return f"Customer(customer_id={self.customer_id}, name={self.name}, social_id={self.social_id}, age={self.age}, gender={self.gender}, phone_number={self.phone_number}, balance={self.balance})"
