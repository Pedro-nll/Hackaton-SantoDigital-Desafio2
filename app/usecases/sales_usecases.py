from interfaces.usecases.sales_usecases_interface import Sales_usecases_interface
from interfaces.repositories.sales_repository_interface import Sales_database_interface
from interfaces.usecases.productsUsecasesInterface import ProductsUsecasesInterface
from interfaces.usecases.customers_usecases_interface import Customers_usecases_interface
from interfaces.usecases.territories_usecases_interface import Territory_usecases_interface
from entities.sales import Sale
from entities.product import Product
from entities.customer import Customer

class Sales_usecases(Sales_usecases_interface):
    def __init__(self, repository: Sales_database_interface, product_usecases: ProductsUsecasesInterface, customer_usecases: Customers_usecases_interface, territory_usecases: Territory_usecases_interface):
        self.repository = repository
        self.product_usecases = product_usecases
        self.customer_usecases = customer_usecases
        self.territory_usecases = territory_usecases
   
    def add_sale(self, sale: Sale):
        self.repository.add_sale(sale)

    def top_products_for_category(self, category: str) -> list[Product]:
        product_keys = self.repository.top_products_for_category(category)
        # TODO: N+1
        top_products = list()
        for pk in product_keys:
            product = self.product_usecases.get_product(pk)
            top_products.append(product)
        return top_products
    
    def best_customer(self) -> Customer:
        best_customer_key = self.repository.best_customer()
        return self.customer_usecases.get_customer(best_customer_key)
    
    def busiest_month(self) -> str:
        return self.repository.busiest_month()
    
    def top_sellers(self) -> str:
        top_sellers_keys = self.repository.top_sellers()
        # TODO: n+1 Query model e domain model
        top_sellers = list()
        for pk in top_sellers_keys:
            t = self.territory_usecases.get_territory(pk)
            top_sellers.append(t)
        
        return top_sellers
