from django.db import transaction
from django.http import HttpRequest
from ninja.constants import NOT_SET
from ninja_extra import api_controller, http_get, http_post
from ninja_extra.permissions.common import IsAuthenticated

from src.core.interceptors import AuthBearer
from src.users.repositories import UserRepository
from src.users.schemas import (
    EmailUpdateErrorSchema,
    EmailUpdateSchema,
    EmailUpdateSuccessSchema,
)
from src.users.services import UserService


@api_controller(
    prefix_or_class="/users",
    auth=NOT_SET,
    permissions=[],
    tags=["users"],
)
class UserController:
    repository = UserRepository()
    service = UserService(repository)

    @http_post(
        "/email/update",
        auth=AuthBearer(),
        permissions=[IsAuthenticated],
        response={
            200: EmailUpdateSuccessSchema,
            400: EmailUpdateErrorSchema,
        },
    )
    @transaction.atomic
    def change_email(self, request: HttpRequest, email_update: EmailUpdateSchema):
        return self.service.change_email(
            email_update=email_update,
            user_id=request.user.pk,
        )
