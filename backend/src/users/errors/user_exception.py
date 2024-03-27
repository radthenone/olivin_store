from ninja_extra import status
from ninja_extra.exceptions import APIException


class UserDoesNotExist(APIException):
    default_detail = "User does not exist"
    status_code = status.HTTP_404_NOT_FOUND


class UsernameAlreadyExists(APIException):
    default_detail = "Username already exists"
    status_code = status.HTTP_409_CONFLICT


class EmailAlreadyExists(APIException):
    default_detail = "Email already exists"
    status_code = status.HTTP_409_CONFLICT
