from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from repositories.sqlite.products_repository import SQLiteProductsRepository
from usecases.product_usecases import ProductUseCases
from entities.product import Product

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = SQLiteProductsRepository('database.db')
product_usecases = ProductUseCases(repository)


@app.post("/products/")
async def create_product(product: Product):
    product_usecases.add_product(product)
    return {"message": "Product added successfully"}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    product_usecases.delete_product(product_id)
    return {"message": "Product deleted successfully"}

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    product.product_id = product_id
    product_usecases.update_product(product)
    return {"message": "Product updated successfully"}

@app.get("/products/{product_id}")
async def read_product(product_id: int):
    product = product_usecases.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/")
async def read_all_products():
    return product_usecases.get_all_products()