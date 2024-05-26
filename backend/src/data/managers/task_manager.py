import logging
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional, Union

from celery.app.base import Celery
from celery.canvas import signature
from celery.schedules import crontab, schedule, solar

from src.core.celery import celery as celery_app

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, client: Celery = celery_app, queue: Optional[str] = None):
        self.celery = client
        self.queue = queue

    def add_to_beat_schedule(self, key: str, value: Any):
        self.celery.conf.beat_schedule[key] = value

    def task(
        self, function: Callable[..., Any], queue: Optional[str] = None
    ) -> Callable[..., Any]:
        task_queue = queue or self.queue

        @self.celery.task(name=function.__name__, queue=task_queue)
        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        def get_result(*a, **k):
            result = wrapper.delay(*a, **k)
            task_result = result.get()
            return task_result

        def get_result_countdown(*a, countdown: Union[timedelta, int] = 0, **k):
            if isinstance(countdown, timedelta):
                countdown = countdown.total_seconds()
            result = wrapper.apply_async(args=a, kwargs=k, countdown=countdown)
            task_result = result.get()
            return task_result

        wrapper.get_result = get_result
        wrapper.get_result_countdown = get_result_countdown
        return wrapper

    def add_task(self, queue: Optional[str] = None) -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            return self.task(function, queue)

        return decorator

    def add_periodic_task(
        self,
        name: str,
        schedule_interval: Union[timedelta, crontab, solar, schedule],
        queue: Optional[str] = None,
    ) -> Callable[..., Any]:
        if not queue:
            queue = self.queue

        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            sig = signature(function.__name__)
            self.celery.add_periodic_task(
                schedule_interval,
                sig,
                name=name,
                options={"queue": queue},
            )

            @wraps(function)
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            def run(*a, **k):
                wrapper(*a, **k)

            wrapper.run = run
            return wrapper

        return decorator
