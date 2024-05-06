from typing import Any, Optional

from src.data.interfaces import ICacheHandler
from src.data.storages import RedisStorage


class CacheHandler(ICacheHandler):
    def __init__(self, pool_storage: RedisStorage, *args, **kwargs):
        super().__init__(pool_storage, *args, **kwargs)
        self.storage = pool_storage

    def get_value(self, key: Any) -> Optional[Any]:
        return self.storage.get(key=key)

    def set_value(self, key: Any, value: Any, expire: Optional[int] = None) -> None:
        self.storage.set(key=key, value=value, expire=expire)

    def delete_value(self, key: Any) -> None:
        self.storage.delete(key=key)

    def exists_all_values(self, key: Any) -> bool:
        return self.storage.exists(key=key)

    def delete_all_values(self) -> None:
        self.storage.flush()
