from src.common import models, tasks  # noqa

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from src.common.routes import common_router
from src.core.celery import celery

api = NinjaAPI()


@celery.task
def connect_celery_task():
    print("Hello, celery!")  # noqa: T201


api.add_router("/common/", common_router, tags=["common"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += []
