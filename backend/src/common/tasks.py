from src.core.celery import celery


@celery.task
def divide(x, y):
    return str(x / y)
