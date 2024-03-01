from ninja import NinjaAPI
from django.http import JsonResponse
import logging


logger = logging.getLogger(__name__)

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    logger.info(msg="Hello World", extra={"request": request.__dict__})
    return JsonResponse({"message": "Hello World"})
