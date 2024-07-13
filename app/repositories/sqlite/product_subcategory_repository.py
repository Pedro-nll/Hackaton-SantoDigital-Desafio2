import sqlite3
from entities.productSubcategories import ProductSubcategory
from interfaces.repositories.productSubcategoriesInterface import ProductsSubcategoriesDatabaseInterface

class SQLiteProductSubcategoriesRepository(ProductsSubcategoriesDatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('PRAGMA foreign_keys = ON;')
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS product_subcategories (
                    product_subcategory_key INTEGER PRIMARY KEY,
                    product_category_key INTEGER,
                    subcategory_name TEXT,
                    FOREIGN KEY (product_category_key) REFERENCES product_categories(product_category_key)
                )'''
            )

    def add_product_subcategory(self, subcategory: ProductSubcategory):
        sql = '''INSERT INTO product_subcategories (product_subcategory_key, product_category_key, subcategory_name) VALUES (?, ?, ?)'''
        params = (subcategory.product_subcategory_key, subcategory.product_category_key, subcategory.subcategory_name)
        self.execute_transaction(sql, params)

    def get_product_subcategory(self, subcategory_key: int) -> ProductSubcategory:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM product_subcategories WHERE product_subcategory_key = ?', (subcategory_key,))
        row = cursor.fetchone()
        return ProductSubcategory(*row) if row else None

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
