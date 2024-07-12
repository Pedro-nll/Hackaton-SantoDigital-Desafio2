from entities.productCategories import ProductCategory
from interfaces.usecases.products_categories_usecases import ProductCategoriesUseCaseInterface
from interfaces.repositories.productCategoriesInterface import ProductsCategoriesDatabaseInterface

class ProductCategoriesUseCase(ProductCategoriesUseCaseInterface):
    def __init__(self, repository: ProductsCategoriesDatabaseInterface):
        self.repository = repository

    def add_product_category(self, category: ProductCategory):
        self.repository.add_product_category(category)

    def get_product_category(self, category_key: int) -> ProductCategory:
        return self.repository.get_product_category(category_key)

