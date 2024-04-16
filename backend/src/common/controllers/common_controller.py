import logging

from django.http import JsonResponse
from ninja_extra import api_controller, http_get, http_post

from src.common.tasks import divide
from src.data.handlers import CacheHandler
from src.data.storages import RedisStorage

logger = logging.getLogger(__name__)


@api_controller(tags=["common"])
class CommonController:
    cache = CacheHandler(RedisStorage())

    @http_get("/")
    def get(self, request):
        return JsonResponse({"message": "hello"})

    @http_post("/ping")
    def ping(self, request):
        self.cache.set_value("ping", "pong", 5)
        return JsonResponse({"message": "make ping"})

    @http_get("/pong")
    def pong(self, request):
        message = self.cache.get_value("ping")
        return JsonResponse({"message": message})

    @http_get("/task")
    def task(self, request):
        result = divide.delay(5, 2)
        return JsonResponse(
            {
                "task_id": result.task_id,
                "message": result.get(),
            }
        )
