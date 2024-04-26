from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Tuple

from celery import Celery
from celery.schedules import crontab, schedule, solar


class TaskManager:
    def __init__(self, celery: Celery, queue: str):
        self.queue = queue
        self.celery = celery

    def task_schedule(
        self,
        queue: str,
        function: Callable[..., Any],
        cycle: crontab | schedule | solar,
        args: Tuple[Any, ...] = (),
        kwargs: Optional[dict] = None,
    ):
        if kwargs is None:
            kwargs = {}
        self.celery.add_periodic_task(
            queue=queue,
            sig=cycle,
            schedule=cycle,
            task=function,
            name=function.__name__,
            args=args,
            kwargs=kwargs,
        )

    def task_interval(
        self,
        queue: str,
        function: Callable[..., Any],
        interval: timedelta,
        args: Tuple[Any, ...] = (),
        kwargs: Optional[dict] = None,
    ):
        if kwargs is None:
            kwargs = {}
        self.celery.send_task(
            queue=queue,
            task=function,
            name=function.__name__,
            args=args,
            kwargs=kwargs,
            countdown=interval.total_seconds(),
        )

    def add_task_schedule(
        self,
        queue: str,
        cycle: crontab,
        args: Tuple[Any, ...] = (),
        kwargs: Optional[dict] = None,
    ):
        if kwargs is None:
            kwargs = {}

        def decorator(function):
            self.task_schedule(
                queue or self.queue,
                function,
                cycle,
                args=args,
                kwargs=kwargs,
            )
            return function

        return decorator

    def add_task_interval(
        self,
        queue: str,
        interval: timedelta,
        args: Tuple[Any, ...] = (),
        kwargs: Optional[dict] = None,
    ):
        if kwargs is None:
            kwargs = {}

        def decorator(function):
            self.task_interval(
                queue or self.queue,
                function,
                interval,
                args=args,
                kwargs=kwargs,
            )
            return function

        return decorator
