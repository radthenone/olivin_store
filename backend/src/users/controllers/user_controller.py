from django.db import transaction
from django.http import HttpRequest, JsonResponse
from ninja.constants import NOT_SET
from ninja_extra import api_controller, http_get, http_post
from ninja_extra.permissions.common import IsAuthenticated

from src.core.interceptors import AuthBearer
from src.data.handlers import EventHandler
from src.data.managers import EventManager
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
    event_handler = EventHandler(manager=EventManager())
    event_handler.sub(["event"])

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

    @http_get("/event/get")
    def get_event(self, request):
        data = self.event_handler.get()
        if data is None:
            data = {"message": "no event"}
        return JsonResponse(data)
