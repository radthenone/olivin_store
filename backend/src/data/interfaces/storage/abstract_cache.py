from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Optional


class ICacheStorage(ABC):
    @abstractmethod
    def set(
        self,
        key: Any,
        value: Any,
        expire: Optional[int | timedelta] = None,
    ) -> bool:
        pass

    @abstractmethod
    def get(
        self,
        key: Any,
    ) -> str:
        pass

    @abstractmethod
    def delete(
        self,
        key: Any,
    ) -> bool:
        pass

    @abstractmethod
    def flush(self) -> bool:
        pass

    @abstractmethod
    def exists(
        self,
        key: Any,
    ) -> bool:
        pass
