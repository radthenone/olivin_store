from src.auth.errors.constants import StatusCodes
from src.common.errors.exceptions import BasicHTTPException


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
