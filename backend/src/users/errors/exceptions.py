from src.common.errors import BasicHTTPException
from src.users.errors.constants import StatusCodes


class NotAuthenticated(BasicHTTPException):
    MESSAGE = "Not authenticated"
    STATUS = StatusCodes.UNAUTHORIZED

    def __init__(self, *args, **kwargs):
        request = kwargs["request"]
        request.headers["Authorization"] = "Barer "
        super().__init__(self.MESSAGE, self.STATUS, *args, **kwargs)


class UserNotFound(BasicHTTPException):
    MESSAGE = "User not found"
    STATUS = StatusCodes.NOT_FOUND
