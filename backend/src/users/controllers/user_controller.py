from ninja.constants import NOT_SET
from ninja_extra import api_controller, http_post

from src.common.utils import Depends
from src.core.interceptors import get_user_id
from src.users.repositories import UserRepository
from src.users.schemas import (
    EmailChangeSchema,
    UserUpdateSchema,
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
        "/email/change",
        response={},
    )
    def change_email(
        self, email_change_schema: EmailChangeSchema, user_id: Depends(get_user_id)
    ):
        return self.service.change_email(
            email_change_schema=email_change_schema,
            user_id=user_id,
        )
