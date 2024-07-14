from abc import ABC, abstractmethod
from entities.sales import Sale
from entities.product import Product
from entities.customer import Customer

class Sales_usecases_interface(ABC):
    @abstractmethod
    def add_sale(self, sale: Sale):
        pass

    @abstractmethod
    def top_products_for_category(self, category: str) -> list[Product]:
        pass
    
    @abstractmethod
    def best_customer(self) -> Customer:
        pass
    
    @abstractmethod
    def busiest_month(self) -> str:
        pass
    
    @abstractmethod
    def top_sellers(self) -> str:
        pass