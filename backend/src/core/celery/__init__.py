from src.core.celery.utils import create_celery

celery = create_celery()

__all__ = ("celery",)
