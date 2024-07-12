from abc import ABC, abstractmethod
from entities.productCategories import ProductCategory

class ProductsCategoriesDatabaseInterface(ABC):
    @abstractmethod
    def add_product_category(self, product_category: ProductCategory):
        pass

    @abstractmethod
    def get_product_category(self, product_category_key: int) -> ProductCategory:
        pass
