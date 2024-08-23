from ninja_extra.exceptions import APIException
from ninja_extra.permissions.common import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, *args, **kwargs):
        if request.auth["username"]:  # type: ignore
            return True

        return False


class LoggedOutOnly(BasePermission):
    def has_permission(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise APIException("Already logged in")

        return True
