from abc import ABC, abstractmethod
from entities.customer import Customer

class customers_database_interface(ABC):
    @abstractmethod
    def add_custormer(self, customer: Customer):
        pass
    
    @abstractmethod
    def get_customer(self, customer_key: int):
        pass