import logging
from datetime import timedelta

from src.data.managers import TaskManager

logger = logging.getLogger(__name__)

task_manager = TaskManager(queue="tasks")
task_manager_schedule = TaskManager(queue="beats")


@task_manager.add_task()
def multiply(a, b):
    logging.info(f"multiply {a} {b}")
    return a * b


@task_manager.add_task(queue="tasks")
def multiply_interval(a, b):
    logging.info(f"multiply_interval {a} {b}")
    return a * b


@task_manager_schedule.add_periodic_task(
    name="multiple by minute",
    schedule_interval=timedelta(minutes=1),
)
def multiply_interval2(a, b):
    logging.info(f"multiply_interval2 {a} {b}")
    return a * b


@task_manager_schedule.add_periodic_task(
    name="value return",
    schedule_interval=timedelta(minutes=2),
)
def value_return(a, b):
    logging.info(f"value_return {a / b}")
    return a / b
