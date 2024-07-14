import sqlite3
from entities.territories import Territory
from interfaces.repositories.territory_repository_interface import territories_database_interface

class SQLiteTerritoriesRepository(territories_database_interface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS territories (
                    salesTerritoryKey INTEGER PRIMARY KEY,
                    region TEXT,
                    country TEXT,
                    continent TEXT
                )'''
            )

    def add_territory(self, territory: Territory):
        sql = '''INSERT INTO territories (salesTerritoryKey, region, country, continent) VALUES (?, ?, ?, ?)'''
        params = (territory.salesTerritoryKey, territory.region, territory.country, territory.continent)
        self.execute_transaction(sql, params)

    def get_territory(self, territory_key: int) -> Territory:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM territories WHERE salesTerritoryKey = ?', (territory_key,))
        row = cursor.fetchone()
        return Territory(*row) if row else None

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
