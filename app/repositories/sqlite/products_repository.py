import sqlite3
from entities.product import Product
from interfaces.repositories.productsDatabaseInterface import ProductsDatabaseInterface

class SQLiteProductsRepository(ProductsDatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('PRAGMA foreign_keys = ON;')
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS products (
                    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_price REAL,
                    product_subcategory_key INTEGER,
                    product_sku TEXT,
                    product_name TEXT,
                    model_name TEXT,
                    product_description TEXT,
                    product_color TEXT,
                    product_size TEXT,
                    product_style TEXT,
                    product_cost REAL,
                    FOREIGN KEY (product_subcategory_key) REFERENCES product_subcategories(product_subcategory_key)
                )'''
            )

    def add_product(self, product: Product):
        sql = '''INSERT INTO products (product_price, product_subcategory_key, product_sku, product_name, model_name, 
                                       product_description, product_color, product_size, product_style, product_cost) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        params = (product.productPrice, product.productSubcategoryKey, product.productSKU, product.productName, 
                  product.modelName, product.productDescription, product.productColor, product.productSize, 
                  product.productStyle, product.productCost)
        self.execute_transaction(sql, params)

    def delete_product(self, product_key: int):
        sql = 'DELETE FROM products WHERE product_key = ?'
        params = (product_key,)
        self.execute_transaction(sql, params)

    def update_product(self, product: Product):
        sql = '''UPDATE products SET product_price = ?, product_subcategory_key = ?, product_sku = ?, product_name = ?, 
                                    model_name = ?, product_description = ?, product_color = ?, product_size = ?, 
                                    product_style = ?, product_cost = ? 
                 WHERE product_key = ?'''
        params = (product.productPrice, product.productSubcategoryKey, product.productSKU, product.productName, 
                  product.modelName, product.productDescription, product.productColor, product.productSize, 
                  product.productStyle, product.productCost, product.productKey)
        self.execute_transaction(sql, params)

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

    def get_product(self, product_key: int) -> Product:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE product_key = ?', (product_key,))
        row = cursor.fetchone()
        return Product(*row) if row else None

    def get_all_products(self) -> list[Product]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        return [Product(*row) for row in rows]

    def __del__(self):
        self.connection.close()
