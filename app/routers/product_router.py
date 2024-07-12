from fastapi import APIRouter, HTTPException
from entities.product import Product
from interfaces.usecases.productsUsecasesInterface import ProductsUsecasesInterface
from schemas.productSchema import ProductSchema

class ProductsRest:
    def __init__(self, product_usecases: ProductsUsecasesInterface):
        self.product_usecases = product_usecases

    def add_routes(self, router: APIRouter):
        router.post("/products/", response_model=dict, tags=["Product"])(self.create_product)
        router.delete("/products/{product_id}", response_model=dict, tags=["Product"])(self.delete_product)
        router.put("/products/{product_id}", response_model=dict, tags=["Product"])(self.update_product)
        router.get("/products/{product_id}", response_model=ProductSchema, tags=["Product"])(self.get_product)
        router.get("/products/", response_model=list[ProductSchema], tags=["Product"])(self.get_all_products)

    async def create_product(self, product: ProductSchema):
        product_entity = Product(**product.model_dump())
        self.product_usecases.add_product(product_entity)
        return {"message": "Product added successfully"}

    async def delete_product(self, product_id: int):
        self.product_usecases.delete_product(product_id)
        return {"message": "Product deleted successfully"}

    async def update_product(self, product_id: int, product: ProductSchema):
        product_entity = Product(product_id=product_id, **product.model_dump(exclude={"product_id"}))
        self.product_usecases.update_product(product_entity)
        return {"message": "Product updated successfully"}

    async def get_product(self, product_id: int):
        product = self.product_usecases.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductSchema.model_validate(product)

    async def get_all_products(self):
        products = self.product_usecases.get_all_products()
        return [ProductSchema.model_validate(product) for product in products]
