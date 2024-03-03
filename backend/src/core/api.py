from ninja import NinjaAPI

from src.common.api import router as common_router

api = NinjaAPI()


api.add_router("/common/", common_router, tags=["common"])
