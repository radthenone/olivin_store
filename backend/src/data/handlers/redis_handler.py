from typing import Any, Optional

from src.data.interfaces import ICacheHandler
from src.data.storages import RedisStorage


class CacheHandler(ICacheHandler):
    def __init__(self, pool_storage: RedisStorage, *args, **kwargs):
        super().__init__(pool_storage, *args, **kwargs)
        self.storage = pool_storage

    def get_value(self, key: Any) -> Optional[Any]:
        return self.storage.cache.get(name=key)

    def set_value(self, key: Any, value: Any, expire: Optional[int] = None) -> None:
        if not expire:
            expire = self.storage.CACHE_EXPIRE

        self.storage.cache.set(name=key, value=value, ex=expire)

    def delete_value(self, key: Any) -> None:
        self.storage.cache.delete(*key)

    def exists_all_values(self, key: Any) -> bool:
        return self.storage.cache.exists(*key)

    def delete_all_values(self) -> None:
        self.storage.cache.flushdb()
