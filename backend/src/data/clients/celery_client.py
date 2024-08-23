import logging
import os

from celery import Celery
from celery.exceptions import CeleryError
from django.apps import apps
from django.conf import settings
from kombu import Exchange, Queue

from src.data.interfaces.client.abstract_client import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


logger = logging.getLogger(__name__)


class CeleryClient(IClient):
    def __init__(
        self,
        main_settings: str,
        broker_url: str,
        result_backend: str,
        timezone: str,
        *args,
        **kwargs,
    ):
        self.celery = self.connect(
            main_settings=main_settings,
            broker_url=broker_url,
            result_backend=result_backend,
            timezone=timezone,
            *args,
            **kwargs,
        )

    def connect(
        self,
        main_settings: str,
        broker_url: str,
        result_backend: str,
        timezone: str,
        *args,
        **kwargs,
    ) -> Celery:
        try:
            celery = Celery(
                main="src.core.celery",
                broker=broker_url,
                backend=result_backend,
                timezone=timezone,
                **kwargs,
            )
            celery.config_from_object(main_settings, namespace="CELERY")

            celery.conf.update(
                task_serializer="json",
                accept_content=["json"],
                result_serializer="json",
                timezone="Europe/Oslo",
                enable_utc=True,
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
                    "result_extended", celery.conf.result_extended
                ),
                task_time_limit=kwargs.get(
                    "task_time_limit", celery.conf.task_time_limit
                ),
                task_soft_time_limit=kwargs.get(
                    "task_soft_time_limit", celery.conf.task_soft_time_limit
                ),
            )

            celery.autodiscover_tasks(settings.INSTALLED_TASKS)

            self.celery = celery
            return self.celery

        except CeleryError as error:
            logger.error(f"Failed to connect to Celery: {error}")
            raise

    def disconnect(self, *args, **kwargs) -> None:
        if self.celery:
            self.celery.close()
