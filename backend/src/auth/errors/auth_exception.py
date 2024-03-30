from ninja_extra import status
from ninja_extra.exceptions import APIException


class UnAuthorized(APIException):
    message = "UnAuthorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpired(APIException):
    default_detail = "Token expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidToken(APIException):
    default_detail = "Invalid token"
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidCredentials(APIException):
    default_detail = "Invalid credentials"
    status_code = status.HTTP_401_UNAUTHORIZED


class AuthorizationFailed(APIException):
    default_detail = "Authorization failed"
    status_code = status.HTTP_401_UNAUTHORIZED


class RefreshTokenRequired(APIException):
    default_detail = "Refresh token required"
    status_code = status.HTTP_401_UNAUTHORIZED
