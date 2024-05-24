from datetime import timedelta
from typing import Any, Optional

from src.data.interfaces import ICacheHandler
from src.data.storages import RedisStorage


class CacheHandler(ICacheHandler):
    """
    Redis cache handler

    Attributes:
        storage (RedisStorage): Redis storage

    Methods:
        get_value(key: Any)
        set_value(key: Any, value: Any, expire: Optional[int] = None)
        delete_value(key: Any)
        exists_all_values(key: Any)
        delete_all_values()

    Usage:
        cache_handler = CacheHandler(pool_storage)
        cache_handler.get_value(key="key")
        cache_handler.set_value(key="key", value="value")
        cache_handler.delete_value(key="key")
        cache_handler.exists_all_values(key="key")
        cache_handler.delete_all_values()
    """

    def __init__(self, pool_storage: RedisStorage, *args, **kwargs):
        super().__init__(pool_storage, *args, **kwargs)
        self.storage = pool_storage

    def get_value(
        self,
        key: Any,
    ) -> Optional[Any]:
        return self.storage.get(key=key)

    def set_value(
        self,
        key: Any,
        value: Any,
        expire: Optional[int | timedelta] = None,
    ) -> None:
        self.storage.set(key=key, value=value, expire=expire)

    def delete_value(
        self,
        key: Any,
    ) -> None:
        self.storage.delete(key=key)

    def exists_all_values(
        self,
        key: Any,
    ) -> bool:
        return self.storage.exists(key=key)

    def delete_all_values(self) -> None:
        self.storage.flush()
