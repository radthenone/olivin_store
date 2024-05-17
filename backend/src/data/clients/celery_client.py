import logging
import os

from celery import Celery
from celery.exceptions import CeleryError
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
        is_events: bool = True,
        *args,
        **kwargs,
    ):
        self.celery = self.connect(
            main_settings=main_settings,
            broker_url=broker_url,
            result_backend=result_backend,
            timezone=timezone,
            is_events=is_events,
            *args,
            **kwargs,
        )

    def connect(
        self,
        main_settings: str,
        broker_url: str,
        result_backend: str,
        timezone: str,
        is_events: bool = True,
        *args,
        **kwargs,
    ) -> Celery:
        try:
            celery = Celery(
                main=main_settings,
                broker_url=broker_url,
                result_backend=result_backend,
                is_events=is_events,
                timezone=timezone,
                **kwargs,
            )
            celery.config_from_object(main_settings, namespace="CELERY")
            celery.conf.update(
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
            celery.autodiscover_tasks()

            self.celery = celery
            return self.celery

        except CeleryError as error:
            logger.error(error)

    def disconnect(self, *args, **kwargs) -> None:
        if self.celery:
            self.celery.close()
