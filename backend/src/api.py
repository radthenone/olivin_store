from django.contrib import admin
from django.urls import path
from ninja.constants import NOT_SET
from ninja_extra import NinjaExtraAPI, api_controller, route

from src.auth.controllers import AuthController
from src.common.controllers import CommonController
from src.core.adds import ApiExtra
from src.core.interceptors import AuthBearer
from src.users.controllers import UserController


def api_imports():  # unused imports
    from src.categories import models, tasks
    from src.common import models, tasks
    from src.events import models, tasks
    from src.files import models, tasks
    from src.orders import models, tasks
    from src.products import models, tasks
    from src.reviews import models, tasks
    from src.users import models, tasks


api_imports()


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
