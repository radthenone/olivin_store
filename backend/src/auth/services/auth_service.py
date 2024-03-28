from typing import Optional

from django.contrib.auth.hashers import check_password

from src.auth.errors import UnAuthorized
from src.auth.schemas import (
    LoginSchema,
    RefreshTokenSchema,
    UserCreateFailedSchema,
    UserCreateSchema,
    UserCreateSuccessSchema,
)
from src.auth.utils import decode_jwt_token, encode_jwt_token
from src.common.responses import ORJSONResponse
from src.common.schemas import MessageSchema
from src.users.errors import EmailAlreadyExists, UserDoesNotExist, UsernameAlreadyExists
from src.users.interfaces import IUserRepository
from src.users.types import UserType


class AuthService:
    def __init__(self, repository: "IUserRepository", *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def authorized_user(
        self,
        username: str,
        password: str,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_username(username=username)
        if user is None:
            raise UserDoesNotExist
        if not check_password(password, user.password):
            raise UnAuthorized
        return user

    def check_user(self, user):
        username = getattr(user, "username", None)
        email = getattr(user, "email", None)

        if username and self.user_repository.get_user_by_username(username=username):
            raise UsernameAlreadyExists

        if email and self.user_repository.get_user_by_email(email=email):
            raise EmailAlreadyExists

    def register_user(
        self,
        user_create: "UserCreateSchema",
    ) -> Optional["ORJSONResponse"]:
        self.check_user(user=user_create)
        if self.user_repository.create_user(
            user_create=user_create,
        ):
            return ORJSONResponse(
                data=UserCreateSuccessSchema().model_dump(),
                status=201,
            )
        return ORJSONResponse(
            data=UserCreateFailedSchema().model_dump(),
            status=400,
        )

    def login_user(
        self,
        username: str,
        password: str,
    ) -> Optional["ORJSONResponse"]:
        try:
            user = self.authorized_user(username, password)
            token = encode_jwt_token(user)

            return ORJSONResponse(
                data=LoginSchema(**token).model_dump(),
                status=200,
            )
        except UnAuthorized:
            return ORJSONResponse(
                data=MessageSchema(message="Invalid credentials").model_dump(),
                status=401,
            )

    @staticmethod
    def refresh_token(
        refresh_token: str,
    ) -> Optional["ORJSONResponse"]:
        if not refresh_token:
            return ORJSONResponse(
                data=MessageSchema(message="Refresh token is required").model_dump(),
                status=401,
            )
        decoded_token = decode_jwt_token(token=refresh_token)
        if decoded_token:
            return ORJSONResponse(
                data=RefreshTokenSchema(**decoded_token).model_dump(),
                status=200,
            )
        return ORJSONResponse(
            data=MessageSchema(message="Invalid refresh token").model_dump(),
            status=401,
        )
