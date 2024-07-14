import sqlite3
from entities.user import User
from interfaces.repositories.user_repository_interface import UserDatabaseInterface

class SQLiteUserRepository(UserDatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    role TEXT
                )'''
            )

    def add_user(self, user: User):
        sql = '''INSERT INTO users (username, password, role) VALUES (?, ?, ?)'''
        params = (user.username, user.password, user.role)
        self.execute_transaction(sql, params)

    def get_user(self, username: str) -> User:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        return User(*row) if row else None

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