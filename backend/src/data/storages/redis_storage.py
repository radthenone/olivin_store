import logging
import os
from datetime import timedelta
from typing import Any, Optional

from django.conf import settings

from src.data.clients import RedisClient
from src.data.interfaces import ICacheStorage

logger = logging.getLogger(__name__)


class RedisStorage(ICacheStorage):
    def __init__(self, **kwargs):
        self.storage = RedisClient().connect(**kwargs)

    def get(self, key: Any) -> Optional[Any]:
        return self.storage.get(name=key)

    def set(
        self, key: Any, value: Any, expire: Optional[int | timedelta] = None
    ) -> None:
        if not expire:
            expire = settings.REDIS_EXPIRE

        self.storage.set(name=key, value=value, ex=expire)

    def delete(self, key: Any) -> None:
        self.storage.delete(*key)

    def exists(self, key: Any) -> bool:
        return self.storage.exists(*key)

    def flush(self) -> None:
        self.storage.flushdb()
