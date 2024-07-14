from abc import ABC, abstractmethod
from entities.customer import Customer

class Customers_usecases_interface(ABC):
    @abstractmethod
    def add_customer(self, customer: Customer):
        pass

    @abstractmethod
    def get_customer(self, customer_key: int) -> Customer:
        pass