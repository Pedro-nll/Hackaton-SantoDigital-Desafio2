from fastapi import APIRouter, HTTPException
from entities.product import Product
from interfaces.usecases.productsUsecasesInterface import ProductsUsecasesInterface
from schemas.productSchema import ProductSchema
from schemas.productSubcategorySchema import ProductSubcategorySchema

class ProductsRest:
    def __init__(self, product_usecases: ProductsUsecasesInterface):
        self.product_usecases = product_usecases

    def add_routes(self, router: APIRouter):
        router.post("/products/", response_model=dict, tags=["Product"])(self.create_product)
        router.delete("/products/{product_id}", response_model=dict, tags=["Product"])(self.delete_product)
        router.put("/products/{product_key}", response_model=dict, tags=["Product"])(self.update_product)
        router.get("/products/{product_key}", response_model=ProductSchema, tags=["Product"])(self.get_product)
        router.get("/products/", response_model=list[ProductSchema], tags=["Product"])(self.get_all_products)

    async def create_product(self, product: ProductSchema):
        product_subcategory = product.product_subcategory_key
        if isinstance(product_subcategory, ProductSubcategorySchema):
            product_subcategory = product_subcategory.product_subcategory_key

        product_entity = Product(
            product_key = product.product_key,
            product_price = product.product_price,
            product_subcategory_key = product_subcategory,
            product_sku = product.product_sku,
            product_name = product.product_name,
            model_name = product.product_model_name,
            product_description = product.product_description,
            product_color = product.product_color,
            product_size = product.product_size,
            product_style = product.product_style,
            product_cost = product.product_cost
        )

        self.product_usecases.add_product(product_entity)
        return {"message": "Product added successfully"}


    async def delete_product(self, product_id: int):
        self.product_usecases.delete_product(product_id)
        return {"message": "Product deleted successfully"}

    async def update_product(self, product_key: int, product: ProductSchema):
        product_entity = Product(
                product_key=product_key, 
                product_price = product.product_price,
                product_subcategory_key = product.product_subcategory_key,
                product_sku = product.product_sku,
                product_name = product.product_name,
                model_name = product.product_model_name,
                product_description = product.product_description,
                product_color = product.product_color,
                product_size = product.product_size,
                product_style = product.product_style,
                product_cost = product.product_cost
            )
        self.product_usecases.update_product(product_entity)
        return {"message": "Product updated successfully"}

    async def get_product(self, product_key: int):
        product = self.product_usecases.get_product(product_key)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        print(product.product_key)
        p = ProductSchema(
            product_key = product.product_key,
            product_price = product.product_price,  
            product_subcategory_key = product.product_subcategory_key,
            product_sku = product.product_sku,
            product_name = product.product_name,
            product_model_name = product.model_name,
            product_description = product.product_description,
            product_color = product.product_color,
            product_size = product.product_size,
            product_style = product.product_style,
            product_cost = product.product_cost
        )
        return ProductSchema.model_validate(p)

    async def get_all_products(self):
        products = self.product_usecases.get_all_products()
        
        products_schema_list = list()
        for product in products:
            p = ProductSchema(
                product_price = product.product_price,
                product_key = product.product_key,
                product_subcategory_key = product.product_subcategory_key,
                product_sku = product.product_sku,
                product_name = product.product_name,
                product_model_name = product.model_name,
                product_description = product.product_description,
                product_color = product.product_color,
                product_size = product.product_size,
                product_style = product.product_style,
                product_cost = product.product_cost
            )
            products_schema_list.append(p)
        
        return [ProductSchema.model_validate(product) for product in products_schema_list]
