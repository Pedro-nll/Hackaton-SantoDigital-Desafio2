from abc import ABC, abstractmethod
from entities.sales import Sale

class Sales_database_interface(ABC):
    @abstractmethod
    def add_sale(self, sale: Sale):
        pass
    
    @abstractmethod
    def top_products_for_category(self, category: str):
        pass
    
    @abstractmethod
    def best_customer(self):
        pass
    
    @abstractmethod
    def busiest_month(self):
        pass
    
    @abstractmethod
    def top_sellers(self):
        pass