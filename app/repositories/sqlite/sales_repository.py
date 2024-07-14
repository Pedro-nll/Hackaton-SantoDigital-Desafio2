import sqlite3
from entities.sales import Sale
from interfaces.repositories.sales_repository_interface import Sales_database_interface

class SQLiteSalesRepository(Sales_database_interface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('PRAGMA foreign_keys = ON;')
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS sales (
                    orderNumber INTEGER PRIMARY KEY,
                    productKey INTEGER,
                    customerKey INTEGER,
                    territoryKey INTEGER,
                    orderQuantity INTEGER,
                    orderLineItem INTEGER,
                    orderDate TEXT,
                    stockDate TEXT,
                    FOREIGN KEY (productKey) REFERENCES products(productKey),
                    FOREIGN KEY (customerKey) REFERENCES customers(customerKey),
                    FOREIGN KEY (territoryKey) REFERENCES territories(territoryKey)
                )'''
            )

    def add_sale(self, sale: Sale):
        sql = '''INSERT INTO sales (orderNumber, productKey, customerKey, territoryKey, orderQuantity, orderLineItem, orderDate, stockDate)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        params = (sale.orderNumber, sale.productKey, sale.customerKey, sale.territoryKey,
                  sale.orderQuantity, sale.orderLineItem, sale.orderDate, sale.stockDate)
        self.execute_transaction(sql, params)

    def top_products_for_category(self, category: str):
        #Retorna a chave dos 10 produtos mais vendidos (em quantidade) na categoria fornecida.
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT productKey, SUM(orderQuantity) AS total_quantity
            FROM sales
            WHERE EXISTS (
                SELECT 1 FROM products WHERE products.productKey = sales.productKey AND products.category = ?
            )
            GROUP BY productKey
            ORDER BY total_quantity DESC
            LIMIT 10
        ''', (category,))
        top_products = []
        for row in cursor.fetchall():
            top_products.append(row[0])
        return top_products

    def best_customer(self):
        # Retorna o cliente com o maior número de pedidos realizados.
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT customerKey, SUM(orderQuantity) AS total_quantity
            FROM sales
            GROUP BY customerKey
            ORDER BY total_quantity DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        return row[0] if row else None

    def busiest_month(self):
        # Retorna o mês com mais vendas (em valor total).
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT strftime('%m', s.orderDate) AS month, SUM(p.product_price * s.orderQuantity) AS total_sales
            FROM sales s
            JOIN products p ON s.productKey = p.product_key
            GROUP BY month
            ORDER BY total_sales DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        return row[0] if row else None


    def top_sellers(self):
        # Retorna os vendedores (TERRITORIOS) que tiveram vendas com valor acima da média no último ano fiscal.
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT territoryKey, SUM(product_price * orderQuantity) AS total_sales
            FROM sales s
            JOIN products p ON s.productKey = p.product_key
            WHERE orderDate >= date('now', '-1 year')
            GROUP BY territoryKey
            HAVING total_sales > (SELECT AVG(product_price * orderQuantity) FROM sales WHERE orderDate >= date('now', '-1 year'))
            ORDER BY total_sales DESC
        ''')
        top_sellers = []
        for row in cursor.fetchall():
            top_sellers.append(row[0])
        return top_sellers


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
