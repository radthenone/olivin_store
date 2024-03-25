from ninja_extra import status
from ninja_extra.exceptions import APIException

from src.auth.errors.constants import StatusCodes
from src.common.errors.exceptions import BasicHTTPException


class UnAuthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "UnAuthorized"


class TokenExpired(BasicHTTPException):
    MESSAGE = "Token expired"
    STATUS = StatusCodes.TOKEN_EXPIRED


class InvalidToken(BasicHTTPException):
    MESSAGE = "Invalid token"
    STATUS = StatusCodes.PERMISSION_DENIED


class InvalidCredentials(BasicHTTPException):
    MESSAGE = "Invalid credentials"
    STATUS = StatusCodes.PERMISSION_DENIED


class AuthorizationFailed(BasicHTTPException):
    MESSAGE = "Authorization failed"
    STATUS = StatusCodes.PERMISSION_DENIED
