from django.conf import settings

from src.data.clients import CeleryClient

celery = CeleryClient().connect()

celery.conf.beat_schedule = {
    **settings.CELERY_BEAT_SCHEDULE,
}
