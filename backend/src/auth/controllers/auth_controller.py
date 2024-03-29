from ninja.constants import NOT_SET
from ninja_extra import api_controller, http_post

from src.auth.schemas import (
    LoginSchema,
    RefreshTokenSchema,
    UserCreateFailedSchema,
    UserCreateSchema,
    UserCreateSuccessSchema,
)
from src.auth.services import AuthService
from src.users.repositories import UserRepository


@api_controller(auth=NOT_SET, permissions=[], tags=["auth"])
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
    def register_view(self, user_create: UserCreateSchema):
        return self.service.register_user(user_create=user_create)

    @http_post(
        "/login",
        response={
            200: LoginSchema,
        },
    )
    def login_view(self, username: str, password: str):
        return self.service.login_user(username=username, password=password)

    @http_post("/refresh", response={200: RefreshTokenSchema})
    def refresh_view(self, refresh_token: str):
        return self.service.refresh_token(refresh_token=refresh_token)
