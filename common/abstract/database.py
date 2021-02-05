from abc import ABC, abstractmethod


class DBConnection(ABC):
    @classmethod
    def __enter__(self):
        raise NotImplementedError()

    @classmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @abstractmethod
    def cursor(self):
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()
