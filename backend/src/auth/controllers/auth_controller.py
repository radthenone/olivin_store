from django.db import transaction
from ninja.constants import NOT_SET
from ninja_extra import api_controller, http_post

from src.auth.schemas import (
    LoginSchema,
    LoginSchemaFailed,
    LoginSchemaSuccess,
    RefreshTokenSchema,
    RefreshTokenSchemaFailed,
    RefreshTokenSchemaSuccess,
    UserCreateFailedSchema,
    UserCreateSchema,
    UserCreateSuccessSchema,
)
from src.auth.services import AuthService
from src.users.repositories import UserRepository


@api_controller(
    prefix_or_class="/auth",
    auth=NOT_SET,
    permissions=[],
    tags=["auth"],
)
class AuthController:
    repository = UserRepository()
    service = AuthService(repository)

    @http_post(
        "/register",
        response={
            201: UserCreateSuccessSchema,
            400: UserCreateFailedSchema,
        },
    )
    @transaction.atomic
    def register_view(self, user_create: UserCreateSchema):
        return self.service.register_user(
            user_create=user_create,
        )

    @http_post(
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

    @http_post(
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
