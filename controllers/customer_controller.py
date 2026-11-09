from controllers.error_handler import handle_errors
from models.customer import Customer
from validation.validation import Validation


class CustomerController:
    def __init__(self, customer_service):
        self.__service = customer_service

    @handle_errors
    def save(self, customer_id, name, social_id, age, gender, phone_number, balance):
        customer = Customer(customer_id, name, social_id, age, gender, phone_number, balance)
        self.__service.save(customer)
        return True, f"Info : Customer {customer.name} Saved"

    @handle_errors
    def get_by_id(self, customer_id):
        customer = self.__service.get_by_id(Validation.id_number(customer_id, "Customer ID"))
        return True, customer

    @handle_errors
    def add_balance(self, customer_id, amount):
        customer_id = Validation.id_number(customer_id, "Customer ID")
        self.__service.add_balance(customer_id, amount)
        return True, f"Info : Balance Added to Customer {customer_id}"
