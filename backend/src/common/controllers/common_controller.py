import logging
from typing import Any, Callable, TypeVar

from django.core.cache import cache
from django.http import JsonResponse
from ninja_extra import api_controller, http_get, http_post

from src.common.tasks import divide

T = TypeVar("T", bound=Callable[[Any], Any])

logger = logging.getLogger(__name__)


@api_controller(tags=["common"])
class CommonController:
    @http_get("/")
    def get(self, request):
        print(request.user)
        print(request.auth)
        return JsonResponse({"message": "hello"})

    @http_post("/ping")
    def ping(self, request):
        cache.set("ping", "pong", 5)
        return JsonResponse({"message": "make ping"})

    @http_get("/pong")
    def pong(self, request):
        message = cache.get("ping")
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
