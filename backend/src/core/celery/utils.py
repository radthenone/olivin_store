import os

from celery import Celery
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


def create_celery():
    celery_app = Celery(
        f"{settings}",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )
    celery_app.config_from_object(settings, namespace="CELERY")
    celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

    return celery_app
