import logging

from django.http import JsonResponse
from ninja_extra import api_controller, http_get, http_post

from src.common.tasks import (
    multiply,
    multiply_interval,
    multiply_interval2,
    value_return,
)
from src.data.handlers import CacheHandler, EventHandler
from src.data.managers import EventManager
from src.data.storages import RedisStorage

logger = logging.getLogger(__name__)


@api_controller(tags=["common"])
class CommonController:
    cache = CacheHandler(RedisStorage())
    event_handler = EventHandler(manager=EventManager())

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

    @http_get("/task2")
    def task2(self):
        result = multiply.get_result(10, 2)
        result2 = multiply_interval.get_result(10, 2)
        multiply_interval2.run(10, 2)
        value_return.run(10, 2)
        return JsonResponse(
            {
                "result": result,
                "result2": result2,
            }
        )

    @http_post("/event")
    def event(self, request):
        self.event_handler.pub("event", {"message": "hello"})
        return JsonResponse({"message": "make event"})
