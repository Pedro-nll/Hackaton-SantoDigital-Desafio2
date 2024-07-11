from fastapi import APIRouter, HTTPException
from entities.product import Product
from usecases.product_usecases import ProductUseCases

class ProductsRest:
    def __init__(self, product_usecases: ProductUseCases):
        self.product_usecases = product_usecases

    def add_routes(self, router: APIRouter):
        router.post("/products/")(self.create_product)
        router.delete("/products/{product_id}")(self.delete_product)
        router.put("/products/{product_id}")(self.update_product)
        router.get("/products/{product_id}")(self.read_product)
        router.get("/products/")(self.read_all_products)

    async def create_product(self, product: Product):
        self.product_usecases.add_product(product)
        return {"message": "Product added successfully"}

    async def delete_product(self, product_id: int):
        self.product_usecases.delete_product(product_id)
        return {"message": "Product deleted successfully"}

    async def update_product(self, product_id: int, product: Product):
        product.product_id = product_id
        self.product_usecases.update_product(product)
        return {"message": "Product updated successfully"}

    async def read_product(self, product_id: int):
        product = self.product_usecases.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def read_all_products(self):
        return self.product_usecases.get_all_products()
