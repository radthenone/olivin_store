from ninja_extra import status
from ninja_extra.exceptions import APIException


class ProfileDoesNotExist(APIException):
    default_detail = "Profile does not exist"
    status_code = status.HTTP_404_NOT_FOUND


class ProfileNotFound(APIException):
    default_detail = "Profile not found"
    status_code = status.HTTP_404_NOT_FOUND
