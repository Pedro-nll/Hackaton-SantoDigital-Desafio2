import csv
import requests
import pandas as pd
from typing import Union
from pydantic import BaseModel

# Define schemas
class ProductCategorySchema(BaseModel):
    product_category_key: int
    category_name: str

class ProductSubcategorySchema(BaseModel):
    product_subcategory_key: int
    subcategory_name: str
    product_category_key: Union[int, ProductCategorySchema]

class ProductSchema(BaseModel):
    product_price: float
    product_key: int
    product_subcategory_key: Union[int, ProductSubcategorySchema]
    product_sku: str
    product_name: str
    product_model_name: str
    product_description: str
    product_color: str
    product_size: str
    product_style: str
    product_cost: float

class TerritorySchema(BaseModel):
    salesTerritoryKey: int
    region: str
    country: str
    continent: str

class CustomerSchema(BaseModel):
    educationLevel: str
    occupation: str
    homeOwner: bool
    customerKey: int
    prefix: str
    firstName: str
    lastName: str
    birthDate: str
    maritalStatus: str
    gender: str
    emailAddress: str
    annualIncome: float
    totalChildren: int

class SaleSchema(BaseModel):
    orderNumber: str
    productKey: int
    customerKey: int
    territoryKey: int
    orderQuantity: int
    orderLineItem: int
    orderDate: str
    stockDate: str
    
def get_jwt_token():
    login_data = {
        "username": "teste",
        "password": "123",
        "role": ""
    }
    response = requests.post('http://127.0.0.1:8000/login', json=login_data)
    response.raise_for_status()
    return response.json().get('access_token')


token = get_jwt_token()
headers = {'Authorization': f'Bearer {token}'}

# Define functions to post data
def post_category(category_key, category_name):
    category = ProductCategorySchema(
        product_category_key=category_key,
        category_name=category_name
    )
    try:
        response = requests.post('http://127.0.0.1:8000/categories/', json=category.dict())
        response.raise_for_status()
    except requests.HTTPError:
        pass

def post_subcategory(subcategory_key, subcategory_name, category):
    subcategory = ProductSubcategorySchema(
        product_subcategory_key=subcategory_key,
        subcategory_name=subcategory_name,
        product_category_key=category
    )
    try:
        response = requests.post('http://127.0.0.1:8000/subcategories/', json=subcategory.dict())
        response.raise_for_status()
    except requests.HTTPError:
        pass

def post_product(product):
    try:
        response = requests.post('http://127.0.0.1:8000/products/', json=product.dict(), headers=headers)
        response.raise_for_status()
    except requests.HTTPError:
        pass

def post_territory(territory):
    try:
        response = requests.post('http://127.0.0.1:8000/territories/', json=territory.dict())
        response.raise_for_status()
    except requests.HTTPError:
        pass

def post_customer(customer):
    try:
        response = requests.post('http://127.0.0.1:8000/customers/', json=customer.dict())
        response.raise_for_status()
    except requests.HTTPError:
        pass

def post_sale(sale):
    try:
        response = requests.post('http://127.0.0.1:8000/sales/', json=sale.dict())
        response.raise_for_status()
    except requests.HTTPError:
        pass

# Process territories
def process_territories():
    territories_df = pd.read_csv('./docs/Data/AdventureWorks_Territories.csv', encoding='ISO-8859-1')
    for _, row in territories_df.iterrows():
        territory = TerritorySchema(
            salesTerritoryKey=int(row['SalesTerritoryKey']),
            region=row['Region'],
            country=row['Country'],
            continent=row['Continent']
        )
        post_territory(territory)

# Process customers
def process_customers():
    customers_df = pd.read_csv('./docs/Data/AdventureWorks_Customers.csv', encoding='ISO-8859-1')
    for _, row in customers_df.iterrows():
        annual_income_str = row['AnnualIncome'].replace('$', '').replace(',', '')
        annual_income = float(annual_income_str)
        home_owner = row['HomeOwner'].strip().upper() == 'Y'
        
        customer = CustomerSchema(
            customerKey=int(row['CustomerKey']),
            prefix=row['Prefix'] if pd.notna(row['Prefix']) else '',
            firstName=row['FirstName'] if pd.notna(row['FirstName']) else '',
            lastName=row['LastName'] if pd.notna(row['LastName']) else '',
            birthDate=row['BirthDate'] if pd.notna(row['BirthDate']) else '',
            maritalStatus=row['MaritalStatus'] if pd.notna(row['MaritalStatus']) else '',
            gender=row['Gender'] if pd.notna(row['Gender']) else '',
            emailAddress=row['EmailAddress'] if pd.notna(row['EmailAddress']) else '',
            annualIncome=annual_income,
            totalChildren=int(row['TotalChildren']) if pd.notna(row['TotalChildren']) else 0,
            educationLevel=row['EducationLevel'] if pd.notna(row['EducationLevel']) else '',
            occupation=row['Occupation'] if pd.notna(row['Occupation']) else '',
            homeOwner=home_owner
        )
        post_customer(customer)


# Process sales
def process_sales():
    sales_files = [
        './docs/Data/AdventureWorks_Sales_2015.csv',
        './docs/Data/AdventureWorks_Sales_2016.csv',
        './docs/Data/AdventureWorks_Sales_2017.csv'
    ]
    
    for sales_file in sales_files:
        sales_df = pd.read_csv(sales_file, encoding='ISO-8859-1')
        for _, row in sales_df.iterrows():
            sale = SaleSchema(
                orderNumber=row['OrderNumber'],
                productKey=int(row['ProductKey']),
                customerKey=int(row['CustomerKey']),
                territoryKey=int(row['TerritoryKey']),
                orderQuantity=int(row['OrderQuantity']),
                orderLineItem=int(row['OrderLineItem']),
                orderDate=row['OrderDate'],
                stockDate=row['StockDate']
            )
            post_sale(sale)


# Process products
def process_products():
    subcategories_df = pd.read_csv('./docs/Data/AdventureWorks_Product_Subcategories.csv', encoding='ISO-8859-1')
    categories_df = pd.read_csv('./docs/Data/AdventureWorks_Product_Categories.csv', encoding='ISO-8859-1')
    with open('./docs/Data/AdventureWorks_Products.csv', mode='r', newline='', encoding='ISO-8859-1') as products_csv:
        products_reader = csv.DictReader(products_csv)
        for index, row in enumerate(products_reader):
            subcategory_key = int(row['ProductSubcategoryKey'])
            subcategory_row = subcategories_df[subcategories_df['ProductSubcategoryKey'] == subcategory_key].iloc[0]
            category_key = int(subcategory_row['ProductCategoryKey'])
            category_row = categories_df[categories_df['ProductCategoryKey'] == category_key].iloc[0]
            post_category(int(category_row['ProductCategoryKey']), category_row['CategoryName'])
            post_subcategory(int(subcategory_row['ProductSubcategoryKey']), subcategory_row['SubcategoryName'], category_key)
            product = ProductSchema(
                product_key=int(row['ProductKey']),
                product_subcategory_key=int(subcategory_row['ProductSubcategoryKey']),
                product_sku=row['ProductSKU'],
                product_name=row['ProductName'],
                product_model_name=row['ModelName'],
                product_description=row['ProductDescription'],
                product_color=row['ProductColor'],
                product_size=row['ProductSize'],
                product_style=row['ProductStyle'],
                product_cost=float(row['ProductCost']),
                product_price=float(row['ProductPrice'])
            )
            post_product(product)


process_territories()
process_customers()
process_products()
process_sales()

