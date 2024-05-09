import logging
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional, Union

from celery.app import shared_task
from celery.app.base import Celery
from celery.canvas import signature
from celery.local import PromiseProxy
from celery.schedules import crontab, schedule, solar

from src.common.utils import get_full_function_path
from src.core.celery import celery as celery_app

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(
        self,
        celery: Celery = celery_app,
        queue: Optional[str] = None,
    ):
        self.celery = celery
        self.queue = queue
        self.shared_task = shared_task
        self.signature = signature

    def add_to_beat_schedule(self, key: str, value: Any):
        self.celery.conf.beat_schedule[key] = value

    def task(
        self,
        function: Callable[..., Any],
        queue: Optional[str] = None,
        *args,
        **kwargs,
    ) -> PromiseProxy:
        task_name = function.__name__
        task_queue = queue or getattr(self, "queue", None)
        task_args = (args or getattr(self, "args", ()),)
        task_kwargs = (kwargs or getattr(self, "kwargs", {}),)

        task = self.celery.task(
            name=task_name,
            queue=task_queue,
            args=task_args,
            kwargs=task_kwargs,
        )

        return task

    def add_task(
        self,
        queue: Optional[str] = None,
        *args,
        **kwargs,
    ):
        if not queue:
            queue = self.queue

        def decorator(function):
            @wraps(function)
            def wrapper(*a, **k):
                task_result = self.task(
                    function=function,
                    args=a,
                    kwargs=k,
                    queue=queue,
                )(function)

                self.celery.register_task(task=task_result)

                return task_result

            task = wrapper(*args, **kwargs)

            def get_result(*a, **k):
                result = task.delay(*a, **k)
                task_result = result.get()
                return task_result

            wrapper.get_result = get_result
            return wrapper

        return decorator

    def add_periodic_task(
        self,
        name: str,
        schedule_interval: Union[timedelta, crontab, solar, schedule],
        queue: Optional[str] = None,
        *args,
        **kwargs,
    ):
        if not queue:
            queue = self.queue

        def decorator(
            function: Callable[..., Any],
        ):
            sig = self.signature(
                get_full_function_path(function),
                args=args,
                kwargs=kwargs,
            )

            self.celery.add_periodic_task(
                name=name,
                schedule=schedule_interval,
                sig=sig,
                args=args,
                kwargs=kwargs,
                options={
                    "queue": queue or getattr(self, "queue", None),
                },
            )

            @wraps(function)
            def wrapper(*a, **k):
                try:
                    self.add_to_beat_schedule(
                        key=name,
                        value={
                            "task": function.__name__,
                            "schedule": schedule_interval,
                            "args": a,
                            "kwargs": k,
                            "options": {
                                "queue": queue or getattr(self, "queue", None),
                            },
                        },
                    )
                except Exception as e:
                    logger.error(e)

            def run(*a, **k):
                wrapper(*a, **k)

            wrapper.run = run

            return wrapper

        return decorator
