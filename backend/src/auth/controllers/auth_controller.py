from django.http import HttpRequest
from ninja.constants import NOT_SET
from ninja_extra import api_controller, permissions, route, throttle

from src.auth import schemas as auth_schemas
from src.auth.services import AuthService
from src.auth.throttles import RegisterMailThrottle, RegisterThrottle
from src.common import permissions as common_permissions
from src.common import schemas as common_schemas
from src.common.responses import ORJSONResponse
from src.core.handler import get_phone_handler
from src.core.interceptors import AuthBearer
from src.core.storage import get_storage
from src.data.handlers import (
    AvatarFileHandler,
    CacheHandler,
    EventHandler,
    ImageFileHandler,
    RegistrationEmailHandler,
)
from src.data.managers import EventManager, MailManager
from src.data.storages import RedisStorage
from src.users.repositories import ProfileRepository, UserRepository
from src.users.services import ProfileService, UserService


@api_controller(
    prefix_or_class="/auth",
    auth=NOT_SET,
    permissions=[],
    tags=["auth"],
)
class AuthController:
    user_repository = UserRepository()
    profile_repository = ProfileRepository()
    cache_handler = CacheHandler(pool_storage=RedisStorage())
    event_handler = EventHandler(manager=EventManager())
    image_handler = ImageFileHandler(storage=get_storage())

    service = AuthService(
        cache_handler=cache_handler,
        event_handler=event_handler,
        image_handler=image_handler,
        user_service=UserService(
            repository=user_repository,
            event_handler=event_handler,
        ),
        profile_service=ProfileService(
            repository=profile_repository,
            event_handler=event_handler,
            cache_handler=cache_handler,
        ),
    )

    @route.post(
        "/register/mail",
        permissions=[common_permissions.LoggedOutOnly],
    )
    @throttle(RegisterMailThrottle)
    def register_mail_view(
        self,
        user_register_mail_schema: auth_schemas.RegisterUserMailSchema,
    ):
        url_schema = self.service.register_user_mail(
            user_register_mail_schema=user_register_mail_schema,
        )
        return ORJSONResponse(
            data=url_schema.model_dump(),
            status=200,
        )

    @route.post(
        "/register/mail/{token}",
        permissions=[common_permissions.LoggedOutOnly],
    )
    @throttle(RegisterThrottle)
    def register_view(
        self,
        token: str,
        register_schema: auth_schemas.RegisterSchema,
    ):
        register_user_schema = self.service.register_user(
            token=token,
            register_schema=register_schema,
        )
        return ORJSONResponse(
            data=register_user_schema.model_dump(),
            status=200,
        )

    @route.post(
        "/login",
        permissions=[common_permissions.LoggedOutOnly],
    )
    def login_view(
        self,
        login_schema: auth_schemas.LoginSchema,
    ):
        return ORJSONResponse(
            data=self.service.login_user(
                username=login_schema.username,
                password=login_schema.password,
            ).model_dump(),
            status=200,
        )

    @route.post(
        "/refresh",
    )
    def refresh_view(
        self,
        refresh_token_schema: auth_schemas.RefreshTokenSchema,
    ):
        return ORJSONResponse(
            data=self.service.refresh_token(
                refresh_token=refresh_token_schema.refresh_token,
            ).model_dump(),
            status=200,
        )

    @route.post(
        "/logout",
        auth=AuthBearer(),
    )
    def logout_view(
        self,
        request: HttpRequest,
    ):
        request.auth = None
        request.user = None
        return ORJSONResponse(
            data=common_schemas.MessageSchema(message="Logout successful").model_dump(),
            status=200,
        )
