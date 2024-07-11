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
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    price REAL
                )'''
            )

    def add_product(self, product: Product):
        sql = 'INSERT INTO products (product_id, name, description, price) VALUES (?, ?, ?, ?)'
        params = (product.product_id, product.name, product.description, product.price)
        self.execute_transaction(sql, params)

    def delete_product(self, product_id: int):
        sql = 'DELETE FROM products WHERE product_id = ?'
        params = (product_id,)
        self.execute_transaction(sql, params)

    def update_product(self, product: Product):
        sql = 'UPDATE products SET name = ?, description = ?, price = ? WHERE product_id = ?'
        params = (product.name, product.description, product.price, product.product_id)
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

    def get_product(self, product_id: int) -> Product:
        cursor = self.connection.cursor()
        cursor.execute('SELECT product_id, name, description, price FROM products WHERE product_id = ?', (product_id,))
        row = cursor.fetchone()
        return Product(*row) if row else None

    def get_all_products(self) -> list[Product]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT product_id, name, description, price FROM products')
        rows = cursor.fetchall()
        return [Product(*row) for row in rows]

    def __del__(self):
        self.connection.close()
