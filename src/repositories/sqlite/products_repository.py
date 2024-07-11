import sqlite3
from entities.product import Product
from interfaces.repositories.productsDatabaseInterface import DatabaseInterface

class SQLiteProductsRepository(DatabaseInterface):
    def __init__(self, db_path: str):
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
        with self.connection:
            self.connection.execute(
                'INSERT INTO products (product_id, name, description, price) VALUES (?, ?, ?, ?)',
                (product.product_id, product.name, product.description, product.price)
            )

    def delete_product(self, product_id: int):
        with self.connection:
            self.connection.execute(
                'DELETE FROM products WHERE product_id = ?',
                (product_id,)
            )

    def update_product(self, product: Product):
        with self.connection:
            self.connection.execute(
                'UPDATE products SET name = ?, description = ?, price = ? WHERE product_id = ?',
                (product.name, product.description, product.price, product.product_id)
            )

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
