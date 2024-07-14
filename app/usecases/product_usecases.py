from datetime import datetime
from entities.product import Product
from interfaces.usecases.productsUsecasesInterface import ProductsUsecasesInterface
from interfaces.usecases.products_subcategories_usecases import ProductSubcategoriesUseCaseInterface
from interfaces.repositories.productsDatabaseInterface import ProductsDatabaseInterface

class ProductUseCases(ProductsUsecasesInterface):
    def __init__(self, repository: ProductsDatabaseInterface, subcategories_usecases: ProductSubcategoriesUseCaseInterface, logger):
        self.repository = repository
        self.subcategories_usecases = subcategories_usecases
        self.logger = logger

    def add_product(self, product: Product, user: str):
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

        self._log_operation("CREATE", product, user)
        self.repository.add_product(product)

    def delete_product(self, product_id: int, user: str):
        self._log_operation("DELETE", {"product_id": product_id}, user)
        self.repository.delete_product(product_id)

    def update_product(self, product: Product, user: str):
        self._log_operation("UPDATE", product, user)
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
    
    def _log_operation(self, operation, data, user):
        log_message = f"{operation} operation performed by {user.username} at {datetime.now()}: {data}"
        self.logger.info(log_message)
