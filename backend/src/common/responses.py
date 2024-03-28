import orjson
from django.http.response import HttpResponse


class ORJSONResponse(HttpResponse):
    def __init__(self, data, status, encoder=None, safe=True, **kwargs):
        if safe and data is not None and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        if data is not None:
            data = orjson.dumps(data, default=encoder).decode("utf-8")
        kwargs["content_type"] = "application/json"
        self.status_code = status
        super().__init__(content=data, status=status, **kwargs)
