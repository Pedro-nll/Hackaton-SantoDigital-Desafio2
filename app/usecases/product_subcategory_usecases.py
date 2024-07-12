from entities.productSubcategories import ProductSubcategory
from interfaces.usecases.products_subcategories_usecases import ProductSubcategoriesUseCaseInterface
from interfaces.repositories.productSubcategoriesInterface import ProductsSubcategoriesDatabaseInterface

class ProductSubcategoriesUseCase(ProductSubcategoriesUseCaseInterface):
    def __init__(self, repository: ProductsSubcategoriesDatabaseInterface):
        self.repository = repository

    def add_product_subcategory(self, subcategory: ProductSubcategory):
        self.repository.add_product_subcategory(subcategory)

    def get_product_subcategory(self, subcategory_key: int) -> ProductSubcategory:
        return self.repository.get_product_subcategory(subcategory_key)
