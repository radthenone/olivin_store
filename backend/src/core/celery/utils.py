import os

from celery import current_app as current_celery_app
from django.conf import settings
from dotenv import load_dotenv

from src.core.config import PROJECT_DIR

load_dotenv(PROJECT_DIR / ".envs" / ".env")

IS_TYPE = os.getenv("IS_TYPE", "dev")

if IS_TYPE == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings.dev")


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")
    celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

    return celery_app
