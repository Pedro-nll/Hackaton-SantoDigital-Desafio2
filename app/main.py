from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.product_router import ProductsRest
from usecases.product_usecases import ProductUseCases
from repositories.sqlite.products_repository import SQLiteProductsRepository

from repositories.sqlite.product_category_repository import SQLiteProductCategoriesRepository
from usecases.product_category_usecases import ProductCategoriesUseCase
from routers.product_categories_router import ProductCategoriesRest

from repositories.sqlite.product_subcategory_repository import SQLiteProductSubcategoriesRepository
from usecases.product_subcategory_usecases import ProductSubcategoriesUseCase
from routers.product_subcategories_router import ProductSubcategoriesRest

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
categories_usecases = ProductCategoriesUseCase(categories_repository)
categories_rest = ProductCategoriesRest(categories_usecases)
categories_rest.add_routes(app)

subcategories_repository = SQLiteProductSubcategoriesRepository(DB_PATH)
subcategories_usecases = ProductSubcategoriesUseCase(subcategories_repository)
subcategories_rest = ProductSubcategoriesRest(subcategories_usecases)
subcategories_rest.add_routes(app)

products_repository = SQLiteProductsRepository(DB_PATH)
product_usecases = ProductUseCases(products_repository)
products_rest = ProductsRest(product_usecases)
products_rest.add_routes(app)
