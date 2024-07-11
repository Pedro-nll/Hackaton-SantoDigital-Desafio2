from interfaces.repositories.productsDatabaseInterface import DatabaseInterface
from entities.product import Product

class ProductUseCases:
    def __init__(self, repository: DatabaseInterface):
        self.repository = repository

    def add_product(self, product: Product):
        self.repository.add_product(product)

    def delete_product(self, product_id: int):
        self.repository.delete_product(product_id)

    def update_product(self, product: Product):
        self.repository.update_product(product)

    def get_product(self, product_id: int) -> Product:
        return self.repository.get_product(product_id)

    def get_all_products(self) -> list[Product]:
        return self.repository.get_all_products()
