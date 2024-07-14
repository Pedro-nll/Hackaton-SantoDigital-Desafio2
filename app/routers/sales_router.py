from fastapi import APIRouter, HTTPException
from interfaces.usecases.sales_usecases_interface import Sales_usecases_interface

from schemas.sale_schema import Sale_schema
from schemas.productSchema import ProductSchema
from schemas.customer_schema import Customer_schema
from schemas.territory_schema import Territory_schema
from schemas.productCategorySchema import ProductCategorySchema
from schemas.OutputProductSchema import OutputProductSchema
from schemas.OutputProductSubcategorySchema import OutputProductSubcategorySchema

from entities.sales import Sale
from typing import List

class Sales_rest:
    def __init__(self, sales_usecases: Sales_usecases_interface):
        self.sales_usecases = sales_usecases
        
    def add_routes(self, router: APIRouter):
        router.post("/sales/", response_model=dict, tags=["Sales"])(self.add_sale)
        router.post("/sales/top-products/category/{category}", response_model=List[ProductSchema], tags=["Sales"])(self.top_products)
        router.post("/sales/best-customer", response_model=Customer_schema, tags=["Sales"])(self.best_customer)
        router.post("/sales/busiest-month", response_model=dict, tags=["Sales"])(self.busiest_month)
        router.post("/sales/top-sellers", response_model=List[Territory_schema], tags=["Sales"])(self.top_sellers)
    
    async def add_sale(self, sale: Sale_schema):
        sale_entity = Sale(**sale.model_dump())
        self.sales_usecases.add_sale(sale_entity)
        return {"message": "Sale added successfully"}
    
    async def top_products(self, category: str):
        products = self.sales_usecases.top_products_for_category(category)
        products_schema_list = []
        for product in products:
            category_schema = ProductCategorySchema(
                category_name=product.product_subcategory_key.product_category_key.category_name,
                product_category_key=product.product_subcategory_key.product_category_key.product_category_key
            )

            subcategory_schema = OutputProductSubcategorySchema(
                product_subcategory_key=product.product_subcategory_key.product_subcategory_key,
                subcategory_name=product.product_subcategory_key.subcategory_name,
                product_category_key=category_schema
            )

            p = OutputProductSchema(
                product_key=product.product_key,
                product_price=product.product_price,
                product_subcategory_key=subcategory_schema,
                product_sku=product.product_sku,
                product_name=product.product_name,
                product_model_name=product.model_name,
                product_description=product.product_description,
                product_color=product.product_color,
                product_size=product.product_size,
                product_style=product.product_style,
                product_cost=product.product_cost
            )
            products_schema_list.append(p)

        return [OutputProductSchema.model_validate(product) for product in products_schema_list]

    async def best_customer(self):
        customer = self.sales_usecases.best_customer()
        c = Customer_schema(
            educationLevel=customer.educationLevel,
            occupation=customer.occupation,
            homeOwner=customer.homeOwner,
            customerKey=customer.customerKey,
            prefix=customer.prefix,
            firstName=customer.firstName,
            lastName=customer.lastName,
            birthDate=customer.birthDate,
            maritalStatus=customer.maritalStatus,
            gender=customer.gender,
            emailAddress=customer.emailAddress,
            annualIncome=customer.annualIncome,
            totalChildren=customer.totalChildren
        )
        return Customer_schema.model_validate(c)
    
    async def busiest_month(self):
        try:
            month = self.sales_usecases.busiest_month()
            if month is None:
                raise HTTPException(status_code=404, detail="No sales data available.")
            return {"busiest_month": month}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def top_sellers(self):
        top_sellers_entities = self.sales_usecases.top_sellers()
        top_sellers_schema = List()
        for s in top_sellers_entities:
            seller = Territory_schema(
                salesTerritoryKey = s.salesTerritoryKey,
                region=s.region,
                country=s.country,
                continent=s.continent
            ) 
            top_sellers_schema.append(seller)
            
        return [Territory_schema.model_validate(seller) for seller in top_sellers_schema]