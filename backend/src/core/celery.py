from typing import TypeVar

from celery import Celery
from django.conf import settings

from src.data.clients import CeleryClient

CeleryType = TypeVar("CeleryType", bound=Celery)


def get_celery() -> CeleryType:
    client = CeleryClient(
        main_settings=settings.CELERY_SETTINGS,
        broker_url=settings.CELERY_BROKER_URL,
        result_backend=settings.CELERY_RESULT_BACKEND,
        timezone=settings.TIME_ZONE,
        is_events=True,
    )
    return client.celery


celery = get_celery()

celery.conf.beat_schedule = {
    **settings.CELERY_BEAT_SCHEDULE,
}
