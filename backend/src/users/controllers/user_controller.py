import logging

from django.db import transaction
from django.http import HttpRequest, JsonResponse
from ninja.constants import NOT_SET
from ninja_extra import api_controller, route
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

logger = logging.getLogger(__name__)


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

    def event_listener(self):
        self.event_handler.sub(["event"])
        while True:
            data = self.event_handler.get()
            if data:
                text = data["message"]
                logger.info(f"event_listener: {text}")

    @route.post(
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
