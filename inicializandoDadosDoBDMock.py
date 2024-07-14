import csv
import requests
import pandas as pd
from typing import Union
from pydantic import BaseModel, ConfigDict

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

def post_category(category_key, category_name):
    category = ProductCategorySchema(
        product_category_key=category_key,
        category_name=category_name
    )
    a = category.dict()
    try:
        response = requests.post('http://127.0.0.1:8000/categories/', json=a)
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

subcategories_df = pd.read_csv('./docs/Data/AdventureWorks_Product_Subcategories.csv')
categories_df = pd.read_csv('./docs/Data/AdventureWorks_Product_Categories.csv')

def process_csv_data():
    with open('./docs/Data/AdventureWorks_Products.csv', mode='r', newline='', encoding='utf-8-sig') as products_csv:
        products_reader = csv.DictReader(products_csv)

        for index, row in enumerate(products_reader):

            subcategory_key = int(row['ProductSubcategoryKey'])
            
            # Find subcategory row using pandas DataFrame
            subcategory_row = subcategories_df[subcategories_df['ProductSubcategoryKey'] == subcategory_key].iloc[0]
            
            category_key = int(subcategory_row['ProductCategoryKey'])
            
            # Find category row using pandas DataFrame
            category_row = categories_df[categories_df['ProductCategoryKey'] == category_key].iloc[0]
            
            # Post category
            post_category(int(category_row['ProductCategoryKey']), category_row['CategoryName'])
            
            # Post subcategory
            post_subcategory(int(subcategory_row['ProductSubcategoryKey']), subcategory_row['SubcategoryName'], category_key)
            
            # Post product
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

# Function to post product data
def post_product(product):
    try:
        response = requests.post('http://127.0.0.1:8000/products/', json=product.dict())
        response.raise_for_status()
    except requests.HTTPError:
        pass

# Execute the processing function
process_csv_data()
