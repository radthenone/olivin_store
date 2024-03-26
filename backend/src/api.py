from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja.constants import NOT_SET
from ninja.responses import Response
from ninja_extra import NinjaExtraAPI, api_controller, route

from src.auth.utils import AuthBearer
from src.common import models, tasks  # noqa
from src.common.controllers import CommonController


@api_controller(auth=NOT_SET, permissions=[], tags=[])
class APIController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self, request):
        return Response({"token": request.auth})


api = NinjaExtraAPI()

api.register_controllers(
    *[
        APIController,
        CommonController,
    ]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += []
