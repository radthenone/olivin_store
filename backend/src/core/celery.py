from django.conf import settings

from src.data.sessions import get_celery_session

celery = get_celery_session()

celery.conf.beat_schedule = {
    **settings.CELERY_BEAT_SCHEDULE,
}
