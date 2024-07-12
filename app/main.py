from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.product_router import ProductsRest
from usecases.product_usecases import ProductUseCases
from repositories.sqlite.products_repository import SQLiteProductsRepository
from repositories.sqlite.product_category_repository import SQLiteProductCategoriesRepository
from repositories.sqlite.product_subcategory_repository import SQLiteProductSubcategoriesRepository

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

DB_PATH = 'santo.db'

categories_repository = SQLiteProductCategoriesRepository(DB_PATH)

subcategories_repository = SQLiteProductSubcategoriesRepository(DB_PATH)

products_repository = SQLiteProductsRepository(DB_PATH)
product_usecases = ProductUseCases(products_repository)
products_rest = ProductsRest(product_usecases)
products_rest.add_routes(app)
