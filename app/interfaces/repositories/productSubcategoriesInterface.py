from abc import ABC, abstractmethod
from entities.productSubcategories import ProductSubcategory

class ProductsSubcategoriesDatabaseInterface(ABC):
    @abstractmethod
    def add_product_subcategory(self, product_subcategory: ProductSubcategory):
        pass

    @abstractmethod
    def get_product_subcategory(self, product_subcategory_key: int) -> ProductSubcategory:
        pass
