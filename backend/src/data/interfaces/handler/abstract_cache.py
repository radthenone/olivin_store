from abc import ABC, abstractmethod
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Optional, TypeVar

if TYPE_CHECKING:
    from src.data.interfaces import ICacheStorage  # unused import

ICacheStorageType = TypeVar("ICacheStorageType", bound="ICacheStorage")


class ICacheHandler(ABC):
    def __init__(self, pool_storage: ICacheStorageType, *args, **kwargs):
        self.pool_storage = pool_storage

    @abstractmethod
    def get_value(
        self,
        key: Any,
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def set_value(
        self,
        key: Any,
        value: Any,
        expire: Optional[int | timedelta] = None,
    ) -> None:
        pass

    @abstractmethod
    def delete_value(
        self,
        key: Any,
    ) -> None:
        pass

    @abstractmethod
    def exists_all_values(
        self,
        key: Any,
    ) -> bool:
        pass

    @abstractmethod
    def delete_all_values(self) -> None:
        pass
