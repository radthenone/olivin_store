import os

from celery import Celery
from django.conf import settings

from src.data.interfaces.client.abstract_client import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


class CeleryClient(IClient):
    def __init__(
        self,
        main_settings: str = "django.conf:settings",
        broker_url: str = settings.CELERY_BROKER_URL,
        result_backend: str = settings.CELERY_RESULT_BACKEND,
        is_events: bool = True,
        timezone: str = settings.TIME_ZONE,
    ):
        self.main_settings = main_settings
        self.broker_url = broker_url
        self.result_backend = result_backend
        self.is_events = is_events
        self.timezone = timezone
        self.client = None

    def connect(self, **kwargs) -> Celery:
        if not self.client:
            self.client = Celery(
                # main=self.main_settings,
                main="src.core.settings.dev",
                broker_url=self.broker_url,
                result_backend=self.result_backend,
                is_events=self.is_events,
                timezone=self.timezone,
                **kwargs,
            )
            self.client.config_from_object(self.main_settings, namespace="CELERY")
            self.client.autodiscover_tasks()

        return self.client

    def disconnect(self, *args, **kwargs):
        if self.client:
            self.client.close()
