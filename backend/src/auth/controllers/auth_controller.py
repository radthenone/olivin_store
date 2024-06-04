from django.db import transaction
from ninja import File
from ninja.constants import NOT_SET
from ninja.files import UploadedFile
from ninja_extra import api_controller, route, throttle

from src.auth.schemas import (
    LoginSchema,
    LoginSchemaFailed,
    LoginSchemaSuccess,
    RefreshTokenSchema,
    RefreshTokenSchemaFailed,
    RefreshTokenSchemaSuccess,
    RegisterSchema,
    RegisterUserMailSchema,
    RegisterUserMailSchemaSuccess,
    UserCreateFailedSchema,
    UserCreateSchema,
    UserCreateSuccessSchema,
)
from src.auth.services import AuthService
from src.auth.throttles import RegisterMailThrottle, RegisterThrottle
from src.core.storage import get_storage
from src.data.clients import MailClient
from src.data.handlers import (
    CacheHandler,
    EventHandler,
    ImageFileHandler,
    RegistrationEmailHandler,
)
from src.data.managers import EventManager, MailManager
from src.data.storages import RedisStorage
from src.users.repositories import UserRepository


@api_controller(
    prefix_or_class="/auth",
    auth=NOT_SET,
    permissions=[],
    tags=["auth"],
)
class AuthController:
    repository = UserRepository()
    mail_manager = MailManager(client=MailClient())
    cache_handler = CacheHandler(pool_storage=RedisStorage())
    mail_handler = RegistrationEmailHandler(manager=mail_manager)
    image_handler = ImageFileHandler(storage=get_storage())
    event_handler = EventHandler(manager=EventManager())

    service = AuthService(
        repository,
        cache_handler,
        mail_handler,
        image_handler,
        event_handler,
    )

    def event_listener(self):
        self.service.register_profile_response()

    @route.post(
        "/register/mail",
        response={
            200: RegisterUserMailSchemaSuccess,
        },
    )
    @throttle(RegisterMailThrottle)
    @transaction.atomic
    def register_mail_view(
        self,
        user_register: RegisterUserMailSchema,
    ):
        token = self.service.generate_register_token()
        return self.service.register_user_mail(
            token=token,
            user_register=user_register,
        )

    @route.post(
        "/register/mail/{token}",
        response={
            200: UserCreateSuccessSchema,
            400: UserCreateFailedSchema,
        },
    )
    @throttle(RegisterThrottle)
    def register_view(
        self,
        token: str,
        user_register: RegisterSchema,
        avatar: UploadedFile = File(...),
    ):
        return self.service.register_user(
            token=token,
            avatar=avatar,
            user_register=user_register,
        )

    @route.post(
        "/login",
        response={
            200: LoginSchemaSuccess,
            400: LoginSchemaFailed,
        },
    )
    def login_view(self, login: LoginSchema):
        return self.service.login_user(
            username=login.username,
            password=login.password,
        )

    @route.post(
        "/refresh",
        response={
            200: RefreshTokenSchemaSuccess,
            400: RefreshTokenSchemaFailed,
        },
    )
    def refresh_view(self, token: RefreshTokenSchema):
        return self.service.refresh_token(
            refresh_token=token.refresh_token,
        )
