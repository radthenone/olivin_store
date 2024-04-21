from celery import Celery
from redis import Redis

from src.data.clients import CeleryClient, RedisClient


def get_redis_session() -> Redis:
    return RedisClient().connect()


def get_celery_session() -> Celery:
    return CeleryClient().connect()
