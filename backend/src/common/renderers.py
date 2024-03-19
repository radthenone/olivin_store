from typing import Any

import orjson
from django.http import HttpRequest
from ninja.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


def json_response(data: Any, status: int) -> bytes:
    request = HttpRequest()
    return ORJSONRenderer().render(
        request=request,
        data=data,
        response_status=status,
    )
