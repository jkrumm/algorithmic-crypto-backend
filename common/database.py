from common.abstract.database import DBConnection
from mysql.connector import connect
import settings


class DatabaseConnection(DBConnection):
    def __init__(self):
        self._connection = None
        self._cursor = None
        self._config = {
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "host": settings.DB_HOST,
            "database": settings.DB_NAME,
            "port": settings.DB_PORT,
        }

    def __enter__(self):
        self._connection = connect(**self._config)
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cursor is not None:
            self._cursor.close()
        if self._connection is not None:
            self._connection.close()

    def cursor(self):
        self._cursor = self._connection.cursor()
        return self._cursor

    def commit(self):
        self._cursor.commit()

    def rollback(self):
        self._cursor.rollback()
