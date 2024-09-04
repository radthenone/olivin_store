import logging
from typing import Optional
from uuid import UUID

from django.http import HttpRequest, JsonResponse
from ninja import UploadedFile
from ninja.constants import NOT_SET
from ninja_extra import api_controller, route
from ninja_extra.exceptions import APIException
from ninja_extra.permissions.common import IsAuthenticated

from src.common.responses import ORJSONResponse
from src.common.schemas import MessageSchema
from src.core.config import get_phone_handler, get_storage
from src.core.interceptors import AuthBearer
from src.data.handlers import AvatarFileHandler, CacheHandler, EventHandler
from src.data.managers import EventManager
from src.data.storages import RedisStorage
from src.files.services import FileService
from src.users import errors as users_errors
from src.users import schemas as users_schemas
from src.users.repositories import ProfileRepository, UserRepository
from src.users.services import ProfileService, UserService

logger = logging.getLogger(__name__)


@api_controller(
    prefix_or_class="/users",
    auth=NOT_SET,
    permissions=[],
    tags=["users"],
)
class UsersController:
    user_repository = UserRepository()
    profile_repository = ProfileRepository()
    avatar_handler = AvatarFileHandler(storage=get_storage())
    cache_handler = CacheHandler(pool_storage=RedisStorage())
    event_handler = EventHandler(manager=EventManager())
    phone_handler = get_phone_handler(
        cache=cache_handler,
        repository=profile_repository,
    )

    file_service = FileService(
        avatar_handler=avatar_handler,
    )

    user_service = UserService(
        repository=user_repository,
        avatar_handler=avatar_handler,
        event_handler=event_handler,
    )

    profile_service = ProfileService(
        repository=profile_repository,
        event_handler=event_handler,
        cache_handler=cache_handler,
        avatar_handler=avatar_handler,
        phone_handler=phone_handler,
    )

    @route.get(
        "/account",
        auth=AuthBearer(),
    )
    def get_account(
        self,
        request: HttpRequest,
    ):
        try:
            user_schema = self.user_service.get_user(user_id=request.user.pk)
            if user_schema:
                profile_schema = self.profile_service.get_profile(
                    user_id=request.user.pk
                )
                avatar = self.file_service.get_avatar_url(avatar_key=request.user.pk)
                return ORJSONResponse(
                    data={
                        **user_schema.model_dump(),
                        **profile_schema.model_dump(),
                        "avatar": avatar,
                    },
                    status=200,
                )

        except APIException:
            raise users_errors.UserNotFound

    @route.post(
        path="/update/email",
        auth=AuthBearer(),
        permissions=[IsAuthenticated],
    )
    def change_email(
        self,
        request: HttpRequest,
        email_update_schema: users_schemas.EmailUpdateSchema,
    ):
        return ORJSONResponse(
            data=self.user_service.change_email(
                email_update_schema=email_update_schema,
                user_id=request.user.pk,
            ).model_dump(),
            status=200,
        )
