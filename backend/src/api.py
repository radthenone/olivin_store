from src.common import models, tasks  # noqa

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from src.common.routes import common_router
from src.core.celery import celery
from src.core.interceptors.auth_interceptors import AuthBearer
from src.common.responses import ORJSONResponse
from src.auth.utils import get_token_from_request
from src.common.utils import Depends

api = NinjaAPI()

api.renderers = {
    "default": "src.common.renderers.ORJSONRenderer",
}


@celery.task
def connect_celery_task():
    print("Hello, celery!")


api.add_router("/common/", common_router, tags=["common"])


@api.get("/bearer", auth=AuthBearer())
def bearer(
    request,
    token: str = Depends(get_token_from_request),
):
    if request.auth is None:
        return ORJSONResponse(
            data={"message": "Unauthorized"},
            status_code=401,
        )
    return ORJSONResponse(
        {"token": token},
        status_code=200,
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += []
