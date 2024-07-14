from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from routers.product_router import ProductsRest
from usecases.product_usecases import ProductUseCases
from repositories.sqlite.products_repository import SQLiteProductsRepository

from repositories.sqlite.product_category_repository import SQLiteProductCategoriesRepository
from usecases.product_category_usecases import ProductCategoriesUseCase
from routers.product_categories_router import ProductCategoriesRest

from repositories.sqlite.product_subcategory_repository import SQLiteProductSubcategoriesRepository
from usecases.product_subcategory_usecases import ProductSubcategoriesUseCase
from routers.product_subcategories_router import ProductSubcategoriesRest

from repositories.sqlite.sqlite_user_repository import SQLiteUserRepository
from usecases.user_usecase import UserUseCase
from routers.login_router import LoginRest

from repositories.sqlite.customers_repository import SQLiteCustomersRepository

from repositories.sqlite.territories_repository import SQLiteTerritoriesRepository

from repositories.sqlite.sales_repository import SQLiteSalesRepository

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = 'santo.db'

user_repository = SQLiteUserRepository(DB_PATH)
user_usecase = UserUseCase(user_repository)
login_rest = LoginRest(user_usecase)
login_rest.add_routes(app)

categories_repository = SQLiteProductCategoriesRepository(DB_PATH)
categories_usecases = ProductCategoriesUseCase(categories_repository)
categories_rest = ProductCategoriesRest(categories_usecases)
categories_rest.add_routes(app)

subcategories_repository = SQLiteProductSubcategoriesRepository(DB_PATH)
subcategories_usecases = ProductSubcategoriesUseCase(subcategories_repository, categories_usecases)
subcategories_rest = ProductSubcategoriesRest(subcategories_usecases)
subcategories_rest.add_routes(app)

products_repository = SQLiteProductsRepository(DB_PATH)
product_usecases = ProductUseCases(products_repository, subcategories_usecases, logger)
products_rest = ProductsRest(product_usecases)
products_rest.add_routes(app)

customers_repository = SQLiteCustomersRepository(DB_PATH)

territories_repository = SQLiteTerritoriesRepository(DB_PATH)

sales_repository = SQLiteSalesRepository(DB_PATH)
