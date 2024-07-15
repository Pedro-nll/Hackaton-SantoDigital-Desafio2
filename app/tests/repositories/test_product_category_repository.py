import pytest
import sqlite3
from entities.productCategories import ProductCategory
from repositories.sqlite.product_category_repository import SQLiteProductCategoriesRepository

@pytest.fixture
def db():
    return ':memory:'

@pytest.fixture
def repository(db):
    return SQLiteProductCategoriesRepository(db)

def test_add_and_get_product_category(repository):
    category = ProductCategory(
        product_category_key=1,
        category_name='Electronics'
    )
    
    repository.add_product_category(category)
    
    retrieved_category = repository.get_product_category(1)
    
    assert retrieved_category.product_category_key == category.product_category_key
    assert retrieved_category.category_name == category.category_name
