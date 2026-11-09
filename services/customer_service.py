from utils.logger import logger
from validation.validation import Validation


class CustomerService:
    def __init__(self, customer_data_access):
        self.__data_access = customer_data_access

    def save(self, customer):
        if self.__data_access.get_by_id(customer.customer_id) is not None:
            raise ValueError("Customer ID already exists.")
        self.__data_access.save(customer)
        logger.info(f"Customer {customer.customer_id} created")

    def get_by_id(self, customer_id):
        customer = self.__data_access.get_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")
        return customer

    def add_balance(self, customer_id, amount):
        customer = self.get_by_id(customer_id)
        amount = Validation.money(amount, "Amount")
        customer.balance = customer.balance + amount
        self.__data_access.edit(customer)
        logger.info(f"Balance of customer {customer_id} increased by {amount}")
