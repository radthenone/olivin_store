from typing import Optional

from django.contrib.auth.hashers import check_password
from ninja.security import HttpBearer

from src.common.responses import ORJSONResponse
from src.users.errors import (
    EmailAlreadyExists,
    NotAuthenticated,
    UserNotFound,
)
from src.users.schemas import (
    UserCreateSchema,
)
from src.users.types import UserType


class AuthService:
    def __init__(self, repository, *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def is_authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_username(username)
        if user is None:
            raise UserNotFound
        if not check_password(password, user.password):
            raise NotAuthenticated
        return user

    def is_abstract_user(
        self,
        username: str,
        password: str,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_username(username)
        if user is None:
            raise UserNotFound
        if not check_password(password, user.password):
            raise NotAuthenticated
        return user

    def register_user(
        self,
        user_create: "UserCreateSchema",
    ) -> Optional["ORJSONResponse"]:
        if self.user_repository.get_user_by_email(
            email=user_create.email,
        ):
            raise EmailAlreadyExists

        if self.user_repository.create_user(
            user_create=user_create,
        ):
            return ORJSONResponse(
                data=UserCreateSuccessSchema(
                    message="User created successfully"
                ).model_dump(),
                status=201,
            )
