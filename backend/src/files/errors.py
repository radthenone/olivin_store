from ninja_extra import status
from ninja_extra.exceptions import APIException


class AvatarNotFound(APIException):
    default_detail = "Avatar not found"
    status_code = status.HTTP_404_NOT_FOUND


class AvatarExists(APIException):
    default_detail = "Avatar already exists"
    status_code = status.HTTP_400_BAD_REQUEST


class AvatarUploadFailed(APIException):
    default_detail = "Avatar upload failed"
    status_code = status.HTTP_400_BAD_REQUEST


class AvatarDeleteFailed(APIException):
    default_detail = "Avatar deletion failed"
    status_code = status.HTTP_400_BAD_REQUEST


class AvatarUpdateFailed(APIException):
    default_detail = "Avatar update failed"
    status_code = status.HTTP_400_BAD_REQUEST
