from abc import ABC, abstractmethod
from entities.productCategories import ProductCategory

class ProductCategoriesUseCaseInterface(ABC):
    @abstractmethod
    def add_product_category(self, category: ProductCategory):
        pass

    @abstractmethod
    def get_product_category(self, category_key: int) -> ProductCategory:
        pass
