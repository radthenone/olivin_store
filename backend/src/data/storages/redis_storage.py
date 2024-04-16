import logging
import os
from typing import Optional

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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.decode_responses = decode_responses
        self.cache: Optional[Redis] = None
        self.connect()

    def connect(self):
        if not self.cache:
            self.cache = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=self.decode_responses,
            )

    def disconnect(self):
        if self.cache:
            self.cache.close()
            self.cache = None
