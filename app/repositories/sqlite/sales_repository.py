import sqlite3
from entities.sales import Sale
from interfaces.repositories.sales_repository_interface import Sales_database_interface
from datetime import datetime
from collections import defaultdict

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
                    orderNumber TEXT PRIMARY KEY,
                    productKey INTEGER,
                    customerKey INTEGER,
                    territoryKey INTEGER,
                    orderQuantity INTEGER,
                    orderLineItem INTEGER,
                    orderDate TEXT,
                    stockDate TEXT,
                    FOREIGN KEY (productKey) REFERENCES products(product_key),
                    FOREIGN KEY (customerKey) REFERENCES customers(customerKey),
                    FOREIGN KEY (territoryKey) REFERENCES territories(salesTerritoryKey)
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
                SELECT 1 FROM products WHERE products.product_key = sales.productKey 
                AND products.product_subcategory_key = (SELECT product_subcategories.product_subcategory_key 
                                                        FROM product_subcategories 
                                                        WHERE product_subcategories.product_category_key = (SELECT product_category_key 
                                                                                                            FROM product_categories 
                                                                                                            WHERE category_name = ?))
                
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
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT s.orderDate, p.product_price, s.orderQuantity
            FROM sales s
            JOIN products p ON s.productKey = p.product_key
        ''')
        rows = cursor.fetchall()

        sales_per_month = defaultdict(float)
        for orderDate, product_price, orderQuantity in rows:
            try:
                date = datetime.strptime(orderDate, '%m/%d/%Y')
                month = date.strftime('%m')
                sales_per_month[month] += product_price * orderQuantity
            except ValueError as e:
                print(f"Date format error for {orderDate}: {e}")

        busiest_month = max(sales_per_month, key=sales_per_month.get) if sales_per_month else None
        return busiest_month


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
