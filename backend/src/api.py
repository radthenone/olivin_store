from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest
from django.urls import path
from ninja.constants import NOT_SET
from ninja_extra import NinjaExtraAPI, api_controller, permissions, route
from ninja_extra.exceptions import APIException

from src.auth.controllers import AuthController
from src.common.controllers import CommonController
from src.common.responses import ORJSONResponse
from src.core.adds import ApiExtra
from src.core.interceptors import AuthBearer
from src.files.controllers import FileController
from src.users.controllers import UsersController


@api_controller(auth=NOT_SET, permissions=[], tags=[])
class APIController:
    @route.get("/bearer", auth=AuthBearer(), permissions=[permissions.IsAuthenticated])
    def bearer(self, request):
        if not request.auth:
            raise APIException(detail="Invalid token", code=401)
        return ORJSONResponse(data=request.auth, status=200)


extra = ApiExtra()

api = NinjaExtraAPI(
    version=extra.VERSION,
    docs_url="/",
)

api.register_controllers(
    *[
        APIController,
        CommonController,
        UsersController,
        AuthController,
        FileController,
    ]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path(f"{extra.PREFIX}/", api.urls),
    path("", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
