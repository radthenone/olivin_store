import os
from typing import Optional

from django.conf import settings
from redis import Redis

from src.data.interfaces import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


class RedisClient(IClient):
    redis: Optional[Redis] = None

    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        password: str = settings.REDIS_PASSWORD,
        db: int = settings.REDIS_DB,
        decode_responses: bool = True,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.decode_responses = decode_responses
        self.redis = self.connect()

    def connect(self, **kwargs) -> Redis:
        self.redis = Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            decode_responses=self.decode_responses,
            **kwargs,
        )

        return self.redis

    def disconnect(self, *args, **kwargs) -> None:
        if self.redis:
            self.redis.close()
