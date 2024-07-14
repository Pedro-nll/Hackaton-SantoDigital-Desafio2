from fastapi import APIRouter
from interfaces.usecases.customers_usecases_interface import Customers_usecases_interface
from schemas.customer_schema import Customer_schema
from entities.customer import Customer

class Customer_rest:
    def __init__(self, customer_usecases: Customers_usecases_interface):
        self.customer_usecases = customer_usecases
        
    def add_routes(self, router: APIRouter):
        router.post("/customers/", response_model=dict, tags=["Customers"])(self.add_customer)
    
    async def add_customer(self, customer: Customer_schema):
        customer_entity = Customer(**customer.model_dump())
        self.customer_usecases.add_customer(customer_entity)
        return {"message": "Customer added successfully"}