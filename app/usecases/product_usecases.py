from entities.product import Product
from interfaces.usecases.productsUsecasesInterface import ProductsUsecasesInterface
from interfaces.usecases.products_subcategories_usecases import ProductSubcategoriesUseCaseInterface
from interfaces.repositories.productsDatabaseInterface import ProductsDatabaseInterface

class ProductUseCases(ProductsUsecasesInterface):
    def __init__(self, repository: ProductsDatabaseInterface, subcategories_usecases: ProductSubcategoriesUseCaseInterface):
        self.repository = repository
        self.subcategories_usecases = subcategories_usecases

    def add_product(self, product: Product):
        all_products = sorted(self.get_all_products(), key=lambda x: x.product_key)
        # GERA UMA KEY NOVA SE FOR NECESSÁRIO
        if product.product_key is None:
            if all_products:
                last_product_key = all_products[-1].product_key
                product.product_key = last_product_key + 1
            else:
                product.product_key = 1
        else:
            # VERIFICA SE A KEY EXISTENTE É ÚNICA
            existing_product = next((p for p in all_products if p.product_key == product.product_key), None)
            if existing_product:
                raise ValueError(f"A product with key {product.product_key} already exists.")


        self.repository.add_product(product)

    def delete_product(self, product_id: int):
        self.repository.delete_product(product_id)

    def update_product(self, product: Product):
        self.repository.update_product(product)

    def get_product(self, product_id: int) -> Product:
        p = self.repository.get_product(product_id)
        p.product_subcategory_key = self.subcategories_usecases.get_product_subcategory(p.product_subcategory_key)
        return p

    def get_all_products(self) -> list[Product]:
        products = self.repository.get_all_products()
        for p in products:
            p.product_subcategory_key = self.subcategories_usecases.get_product_subcategory(p.product_subcategory_key)
        return products
