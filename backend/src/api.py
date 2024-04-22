from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja.constants import NOT_SET
from ninja_extra import NinjaExtraAPI, api_controller, route

from src.auth.controllers import AuthController
from src.common import models, tasks  # unused import
from src.common.controllers import CommonController
from src.core.adds import ApiExtra
from src.core.interceptors import AuthBearer
from src.users.controllers import UserController

# from src.users.models import *
# from src.users.tasks import *


@api_controller(auth=NOT_SET, permissions=[], tags=[])
class APIController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self, request):
        return {"token": request.auth}


extra = ApiExtra()

api = NinjaExtraAPI(
    version=extra.VERSION,
    docs_url="/",
)

api.register_controllers(
    *[
        APIController,
        CommonController,
        AuthController,
        UserController,
    ]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path(f"{extra.PREFIX}/", api.urls),
    path("", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += []
