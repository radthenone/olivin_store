from django.http.request import HttpRequest

from src.common.errors import BasicHTTPException
from src.common.errors.constants import StatusCodes
from src.users.errors.constants import StatusCodes as UserStatusCodes


class NotAuthenticated(BasicHTTPException):
    MESSAGE = "Not authenticated"
    STATUS = UserStatusCodes.UNAUTHORIZED

    def __init__(self, *args, **kwargs):
        request = kwargs["request"]
        request.headers["Authorization"] = "Barer "
        super().__init__(
            request=request, message=self.MESSAGE, status=self.STATUS, *args, **kwargs
        )


class UserNotFound(BasicHTTPException):
    MESSAGE = "User not found"
    STATUS = UserStatusCodes.NOT_FOUND


class UsernameAlreadyExists(BasicHTTPException):
    MESSAGE = "Username already exists"
    STATUS = StatusCodes.CONFLICT


class EmailAlreadyExists(BasicHTTPException):
    MESSAGE = "Email already exists"
    STATUS = StatusCodes.CONFLICT
