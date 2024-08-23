from ninja_extra import status
from ninja_extra.exceptions import APIException


class MailDoesNotSend(APIException):
    default_detail = "Mail does not send"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class NotLoggedIn(APIException):
    default_detail = "Not logged in"
    status_code = status.HTTP_401_UNAUTHORIZED


class UnAuthorized(APIException):
    message = "UnAuthorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpired(APIException):
    default_detail = "Token expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenDoesNotExist(APIException):
    default_detail = "Token does not exist"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidToken(APIException):
    default_detail = "Invalid token"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotFound(APIException):
    default_detail = "User not found"
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
