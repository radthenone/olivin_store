from django.db import transaction
from ninja.constants import NOT_SET
from ninja_extra import api_controller, route, throttle

from src.auth.schemas import (
    LoginSchema,
    LoginSchemaFailed,
    LoginSchemaSuccess,
    RefreshTokenSchema,
    RefreshTokenSchemaFailed,
    RefreshTokenSchemaSuccess,
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
from src.data.handlers import CacheHandler, ImageFileHandler, RegistrationEmailHandler
from src.data.managers import MailManager
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

    service = AuthService(
        repository,
        cache_handler,
        mail_handler,
        image_handler,
    )

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
            201: UserCreateSuccessSchema,
            400: UserCreateFailedSchema,
        },
    )
    @throttle(RegisterThrottle)
    @transaction.atomic
    def register_view(self, user_create: UserCreateSchema, token: str):
        return self.service.register_user(
            token=token,
            user_create=user_create,
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
