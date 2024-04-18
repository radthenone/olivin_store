import logging
import os
from typing import Any, Optional

from django.conf import settings
from redis import Redis

from src.data.interfaces import ICacheStorage

logger = logging.getLogger(__name__)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


class RedisStorage(ICacheStorage):
    CACHE_EXPIRE = settings.REDIS_EXPIRE

    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        password: str = settings.REDIS_PASSWORD,
        db: int = settings.REDIS_DB,
        decode_responses: bool = True,
    ):
        self.storage = Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=decode_responses,
        )

    def get(self, key: Any) -> Optional[Any]:
        return self.storage.get(name=key)

    def set(self, key: Any, value: Any, expire: Optional[int] = None) -> None:
        if not expire:
            expire = self.CACHE_EXPIRE

        self.storage.set(name=key, value=value, ex=expire)

    def delete(self, key: Any) -> None:
        self.storage.delete(*key)

    def exists(self, key: Any) -> bool:
        return self.storage.exists(*key)

    def flush(self) -> None:
        self.storage.flushdb()
