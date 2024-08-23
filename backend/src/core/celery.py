import logging
import logging.config
from typing import TypeVar

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

from src.data.clients import CeleryClient

logger = logging.getLogger(__name__)
CeleryType = TypeVar("CeleryType", bound=Celery)


def get_celery() -> CeleryType:
    client = CeleryClient(
        main_settings=settings.CELERY_SETTINGS,
        broker_url=settings.CELERY_BROKER_URL,
        result_backend=settings.CELERY_RESULT_BACKEND,
        timezone=settings.TIME_ZONE,
    )
    return client.celery


@setup_logging.connect
def config_loggers(*args, **kwargs):
    logging.config.dictConfig(settings.LOGGING)


celery = get_celery()

if celery.connection:
    logger.info("Connected to celery broker")
else:
    logger.error("Failed to connect to celery broker")

celery.conf.beat_schedule = {
    **settings.CELERY_BEAT_SCHEDULE,
}
