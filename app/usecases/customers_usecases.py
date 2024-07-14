from interfaces.usecases.customers_usecases_interface import Customers_usecases_interface
from interfaces.repositories.customers_repository_interface import customers_database_interface
from entities.customer import Customer

class Customer_usecases(Customers_usecases_interface):
    def __init__(self, repository: customers_database_interface):
        self.repository = repository
   
    def add_customer(self, territory: Customer):
        self.repository.add_customer(territory)

    def get_customer(self, customer_key: int) -> Customer:
        return self.repository.get_customer(customer_key)