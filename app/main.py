from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.product_router import ProductsRest
from usecases.product_usecases import ProductUseCases
from repositories.sqlite.products_repository import SQLiteProductsRepository

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

products_repository = SQLiteProductsRepository('database.db')
product_usecases = ProductUseCases(products_repository)
products_rest = ProductsRest(product_usecases)
products_rest.add_routes(app)
