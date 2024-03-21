from typing import Optional

import orjson
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from injector import Injector
from ninja import NinjaAPI
from pydantic import BaseModel

from src.auth.utils import get_token_from_request
from src.common import models, tasks  # noqa
from src.common.renderers import ORJSONRenderer
from src.common.responses import ORJSONResponse
from src.common.routes import common_router
from src.common.utils import Depends
from src.core.celery import celery
from src.core.interceptors.auth_interceptors import AuthBearer

api = NinjaAPI()


@celery.task
def connect_celery_task():
    print("Hello, celery!")


api.add_router("/common/", common_router, tags=["common"])


def get_text():
    return "Hello, world!"


class TokenResponse(BaseModel):
    token: Optional[str]


@api.get("/bearer", response=TokenResponse, include_in_schema=False)
def bearer(
    request,
    token=Depends(get_text),
):
    if token:
        return {"token": token}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += []
