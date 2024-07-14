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
from usecases.customers_usecases import Customer_usecases
from routers.customer_router import Customer_rest

from repositories.sqlite.territories_repository import SQLiteTerritoriesRepository
from usecases.territory_usecases import Territory_usecases
from routers.territory_router import Territory_rest

from repositories.sqlite.sales_repository import SQLiteSalesRepository
from usecases.sales_usecases import Sales_usecases
from routers.sales_router import Sales_rest

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
customers_usecases = Customer_usecases(customers_repository)
customers_rest = Customer_rest(customers_usecases)
customers_rest.add_routes(app)

territories_repository = SQLiteTerritoriesRepository(DB_PATH)
territories_usecases = Territory_usecases(territories_repository)
territories_rest = Territory_rest(territories_usecases)
territories_rest.add_routes(app)

sales_repository = SQLiteSalesRepository(DB_PATH)
sales_usecases = Sales_usecases(sales_repository, product_usecases, customers_usecases, territories_usecases)
sales_rest = Sales_rest(sales_usecases)
sales_rest.add_routes(app)