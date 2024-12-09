import psycopg2
from psycopg2 import sql
from typing import Optional

class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: int = 5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Database connection established.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            self.connection = None

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> None:
        """Execute a single query against the database."""
        if self.connection is None:
            print("Connection not established. Please call connect() first.")
            return
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()

    def fetch_query(self, query: str, params: Optional[tuple] = None) -> list:
        """Fetch results from a query."""
        if self.connection is None:
            print("Connection not established. Please call connect() first.")
            return []
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
