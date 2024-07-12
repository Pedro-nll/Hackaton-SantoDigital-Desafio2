from abc import ABC, abstractmethod
from entities.productSubcategories import ProductSubcategory

class ProductSubcategoriesUseCaseInterface(ABC):
    @abstractmethod
    def add_product_subcategory(self, subcategory: ProductSubcategory):
        pass

    @abstractmethod
    def get_product_subcategory(self, subcategory_key: int) -> ProductSubcategory:
        pass
