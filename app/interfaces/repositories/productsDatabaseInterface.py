from abc import ABC, abstractmethod
from entities.product import Product

class ProductsDatabaseInterface(ABC):
    @abstractmethod
    def add_product(self, product: Product):
        pass
    
    @abstractmethod
    def delete_product(self, product_id: int):
        pass
    
    @abstractmethod
    def update_product(self, product_id: int):
        pass

    @abstractmethod
    def get_product(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def get_all_products(self) -> list[Product]:
        pass