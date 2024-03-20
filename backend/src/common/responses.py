import orjson
from django.http import JsonResponse


class ORJSONResponse(JsonResponse):
    def __init__(self, data=None, encoder=None, **kwargs):
        if data is not None:
            content = orjson.dumps(data, default=encoder).decode("utf-8")
        else:
            content = "{}"
        kwargs["content"] = content
        super().__init__(**kwargs)
