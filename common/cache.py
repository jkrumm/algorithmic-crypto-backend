import redis
from werkzeug.contrib.cache import RedisCache


class Redis:
    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0, password=None
    ):
        self._host = host
        self._port = port
        self._db = db
        self._password = password

    def _connection_pool(self):
        return redis.ConnectionPool(
            host=self._host, port=self._port, db=self._db, password=self._password
        )

    def get_connection(self):
        self._cache = redis.Redis(connection_pool=self._connection_pool())

        return self._cache


class WerkzeugCache:
    def __init__(self, host="localhost", port=6379, db=0, password=None):
        self._host = host
        self._port = port
        self._db = db
        self._password = password

    def get_connection(self):
        self._cache = RedisCache(
            host=self._host, port=self._port, db=self._db, password=self._password,
        )
