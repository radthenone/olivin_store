import logging

from django.core.cache import cache
from django.http import JsonResponse
from ninja import Router

from src.common.tasks import divide, make_divide

logger = logging.getLogger(__name__)

router = Router()


@router.get("/hello")
def hello(request):
    logger.info(msg="Hello World", extra={"request": request.__dict__})
    return JsonResponse({"message": "Hello World"})


@router.post("/ping")
def ping(request):
    cache.set("ping", "pong", 5)
    return JsonResponse({"message": "make ping"})


@router.get("/pong")
def pong(request):
    message = cache.get("ping")
    return JsonResponse({"message": message})


@router.get("/task")
def task(request):
    result = divide.delay(5, 2)
    return JsonResponse(
        {
            "task_id": result.task_id,
            "message": result.get(),
        }
    )


@router.post("/divide/{a}/{b}")
def divide_request(a: int, b: int):
    result = make_divide(a, b)
    return JsonResponse(
        {
            "task_id": result.task_id,
            "message": result.get(),
        }
    )
