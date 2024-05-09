import os

from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue

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
                main=self.main_settings,
                broker_url=self.broker_url,
                result_backend=self.result_backend,
                is_events=self.is_events,
                timezone=self.timezone,
                **kwargs,
            )
            self.client.config_from_object(self.main_settings, namespace="CELERY")
            self.client.conf.update(
                task_queues={
                    "tasks": Queue(
                        "tasks",
                        Exchange("tasks"),
                        routing_key="tasks",
                        queue_arguments={"x-max-priority": 2},
                    ),
                    "events": Queue(
                        "events",
                        Exchange("events"),
                        routing_key="events",
                        queue_arguments={"x-max-priority": 1},
                    ),
                    "beats": Queue(
                        "beats",
                        Exchange("beats"),
                        routing_key="beats",
                        queue_arguments={"x-max-priority": 3},
                    ),
                },
                result_extended=kwargs.get(
                    "result_extended", settings.CELERY_RESULT_EXTENDED
                ),
                task_time_limit=kwargs.get(
                    "task_time_limit", settings.CELERY_TASK_TIME_LIMIT
                ),
                task_soft_time_limit=kwargs.get(
                    "task_soft_time_limit", settings.CELERY_TASK_SOFT_TIME_LIMIT
                ),
            )
            self.client.autodiscover_tasks()

        return self.client

    def disconnect(self, *args, **kwargs) -> None:
        if self.client:
            self.client.close()
