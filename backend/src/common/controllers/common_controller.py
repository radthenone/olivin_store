import logging
import uuid
from datetime import timedelta

from django.http import JsonResponse
from ninja import File, UploadedFile
from ninja_extra import api_controller, http_get, http_post

from src.common.tasks import (
    multiply,
)

logger = logging.getLogger(__name__)


@api_controller(tags=["common"])
class CommonController:
    @http_get("/")
    def get(self, request):
        return JsonResponse({"message": "hello"})

    @http_get("/task2")
    def task2(self):
        result = multiply.delay(2, 3)
        return JsonResponse(
            {
                "result": result,
            }
        )
