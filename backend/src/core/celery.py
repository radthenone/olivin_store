import json
import logging

from celery.app import shared_task
from django.conf import settings

from src.data.sessions import get_celery_session

celery = get_celery_session()
celery.shared_task = shared_task

logging.info("init celery, queue: " + json.dumps(settings.CELERY_BEAT_SCHEDULE))

celery.conf.beat_schedule = {
    **settings.CELERY_BEAT_SCHEDULE,
}
