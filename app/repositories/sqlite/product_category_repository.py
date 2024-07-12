import sqlite3
from entities.productCategories import ProductCategory
from interfaces.repositories.productCategoriesInterface import ProductsCategoriesDatabaseInterface

class SQLiteProductCategoriesRepository(ProductsCategoriesDatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS product_categories (
                    product_category_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT
                )'''
            )

    def add_product_category(self, category: ProductCategory):
        sql = '''INSERT INTO product_categories (category_name) VALUES (?)'''
        params = (category.categoryName,)
        self.execute_transaction(sql, params)

    def get_product_category(self, category_key: int) -> ProductCategory:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM product_categories WHERE product_category_key = ?', (category_key,))
        row = cursor.fetchone()
        return ProductCategory(*row) if row else None

    def execute_transaction(self, sql: str, params: tuple):
        try:
            with self.connection:
                self.connection.execute(sql, params)
        except sqlite3.Error as e:
            print(f"Transaction failed: {e}")
            self.connection.rollback()
            raise
        else:
            self.connection.commit()

    def __del__(self):
        self.connection.close()
