from entities.productSubcategories import ProductSubcategory
from interfaces.usecases.products_categories_usecases import ProductCategoriesUseCaseInterface
from interfaces.usecases.products_subcategories_usecases import ProductSubcategoriesUseCaseInterface
from interfaces.repositories.productSubcategoriesInterface import ProductsSubcategoriesDatabaseInterface

class ProductSubcategoriesUseCase(ProductSubcategoriesUseCaseInterface):
    def __init__(self, repository: ProductsSubcategoriesDatabaseInterface, product_categories_usecases: ProductCategoriesUseCaseInterface):
        self.repository = repository
        self.product_categories_usecases = product_categories_usecases

    def add_product_subcategory(self, subcategory: ProductSubcategory):
        self.repository.add_product_subcategory(subcategory)

    def get_product_subcategory(self, subcategory_key: int) -> ProductSubcategory:
        p_sub = self.repository.get_product_subcategory(subcategory_key)
        p_sub.product_category_key = self.product_categories_usecases.get_product_category(p_sub.product_category_key)
        return p_sub
