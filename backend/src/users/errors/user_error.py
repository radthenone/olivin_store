from ninja_extra import status
from ninja_extra.exceptions import APIException


class UserDoesNotExist(APIException):
    default_detail = "User does not exist"
    status_code = status.HTTP_404_NOT_FOUND


class UserCreateFailed(APIException):
    default_detail = "User create failed"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UserUpdateFailed(APIException):
    default_detail = "User update failed"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class SuperUserCreateFailed(APIException):
    default_detail = "Super user create failed"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class EmailDoesNotExist(APIException):
    default_detail = "Email does not exist"
    status_code = status.HTTP_404_NOT_FOUND


class UsernameAlreadyExists(APIException):
    default_detail = "Username already exists"
    status_code = status.HTTP_409_CONFLICT


class EmailAlreadyExists(APIException):
    default_detail = "Email already exists"
    status_code = status.HTTP_409_CONFLICT


class WrongPassword(APIException):
    default_detail = "Wrong password"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotFound(APIException):
    default_detail = "User not found"
    status_code = status.HTTP_404_NOT_FOUND


class EmailAlreadyInUse(APIException):
    default_detail = "You already have this email"
    status_code = status.HTTP_400_BAD_REQUEST


class WrongOldEmail(APIException):
    default_detail = "Wrong old email"
    status_code = status.HTTP_400_BAD_REQUEST


class EmailUpdateFailed(APIException):
    default_detail = "Email update failed"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
