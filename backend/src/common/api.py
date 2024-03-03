import logging

from django.core.cache import cache
from django.http import JsonResponse
from ninja import Router

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
