import sqlite3
from entities.customer import Customer
from interfaces.repositories.customers_repository_interface import customers_database_interface

class SQLiteCustomersRepository(customers_database_interface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS customers (
                    customerKey INTEGER PRIMARY KEY,
                    educationLevel TEXT,
                    occupation TEXT,
                    homeOwner BOOLEAN,
                    prefix TEXT,
                    firstName TEXT,
                    lastName TEXT,
                    birthDate TEXT,
                    maritalStatus TEXT,
                    gender TEXT,
                    emailAddress TEXT,
                    annualIncome REAL,
                    totalChildren INTEGER
                )'''
            )

    def add_customer(self, customer: Customer):
        sql = '''INSERT INTO customers (customerKey, educationLevel, occupation, homeOwner, prefix, firstName, lastName, birthDate, maritalStatus, gender, emailAddress, annualIncome, totalChildren) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        params = (
            customer.customerKey, customer.educationLevel, customer.occupation, customer.homeOwner,
            customer.prefix, customer.firstName, customer.lastName, customer.birthDate,
            customer.maritalStatus, customer.gender, customer.emailAddress, customer.annualIncome,
            customer.totalChildren
        )
        self.execute_transaction(sql, params)

    def get_customer(self, customer_key: int) -> Customer:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM customers WHERE customerKey = ?', (customer_key,))
        row = cursor.fetchone()
        return Customer(*row) if row else None

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