from typing import Any, Optional

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from ninja.renderers import BaseRenderer

from src.common.errors.constants import StatusCodes


class HTTPException:
    def __init__(
        self,
        request: HttpRequest,
        data: Any,
        *,
        message: Optional[str] = None,
        status: Optional[int] = None,
        renderer: Optional[BaseRenderer] = None,
        temporal_response: Optional[HttpResponse] = None,
    ) -> None:
        self.renderer = renderer
        self.create_response(
            request,
            data,
            message=message,
            status=status,
            temporal_response=temporal_response,
        )

    def get_content_type(self) -> str:
        return f"{self.renderer.media_type}; charset={self.renderer.charset}"

    def create_response(
        self,
        request: HttpRequest,
        data: Any,
        *,
        message: Optional[str] = None,
        status: Optional[int] = None,
        temporal_response: Optional[HttpResponse] = None,
    ) -> HttpResponse:
        if temporal_response:
            status = temporal_response.status_code
        assert status

        if message:
            data["message"] = message
        content = self.renderer.render(request, data, response_status=status)

        if temporal_response:
            response = temporal_response
            response.content = content
        else:
            response = HttpResponse(
                content, status=status, content_type=self.get_content_type()
            )

        return response


class BasicHTTPException(HTTPException):
    MESSAGE: Optional[str] = None
    STATUS: Optional[int] = None

    def __init__(self, request: HttpRequest, data: Any, *args, **kwargs) -> None:
        super().__init__(
            request=request,
            data=data,
            message=self.MESSAGE,
            status=self.STATUS,
            *args,
            **kwargs,
        )


class ServerError(BasicHTTPException):
    MESSAGE = "Internal server error"
    STATUS = StatusCodes.SERVER_ERROR
