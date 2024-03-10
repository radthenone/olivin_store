from datetime import datetime, timedelta

from celery import shared_task
from ninja.errors import HttpError

from src.core.celery import celery

time_start = datetime.now() + timedelta(seconds=60)
time_end = time_start + timedelta(minutes=3)

celery.conf.beat_schedule = {
    "divide": {
        "task": "src.common.tasks.divide",
        "schedule": time_start,
        "options": {"expires": time_end},
    },
}


@shared_task
def divide(x, y):
    return str(x / y)


def make_divide(x, y):
    try:
        result = divide.delay(x, y)
        return result
    except Exception:
        return None
