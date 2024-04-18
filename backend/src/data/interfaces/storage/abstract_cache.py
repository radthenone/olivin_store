from abc import ABC, abstractmethod


class ICacheStorage(ABC):
    @abstractmethod
    def set(self, key: str, value: str, ttl: int = None) -> bool:
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def flush(self) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
