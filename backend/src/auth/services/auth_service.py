from logging import getLogger
from typing import TYPE_CHECKING, Optional

from django.contrib.auth.hashers import check_password

from src.auth.errors import InvalidToken, RefreshTokenRequired, UnAuthorized
from src.auth.schemas import (
    LoginSchemaFailed,
    LoginSchemaSuccess,
    RefreshTokenSchemaFailed,
    RefreshTokenSchemaSuccess,
    UserCreateFailedSchema,
    UserCreateSchema,
    UserCreateSuccessSchema,
)
from src.auth.utils import decode_jwt_token, encode_jwt_token
from src.common.responses import ORJSONResponse
from src.users.errors import (
    EmailAlreadyExists,
    UserDoesNotExist,
    UsernameAlreadyExists,
)

if TYPE_CHECKING:
    from src.users.interfaces import IUserRepository
    from src.users.types import UserType


logger = getLogger(__name__)


class AuthService:
    def __init__(self, repository: "IUserRepository", *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def authorized_user(
        self,
        username: str,
        password: str,
    ) -> Optional["UserType"]:
        logger.debug("AuthService.authorized_user")
        user = self.user_repository.get_user_by_username(username=username)
        if user is None:
            raise UserDoesNotExist
        if not check_password(password, user.password):
            raise UnAuthorized
        logger.info("User %s authorized", user.username)
        return user

    def check_user(self, user):
        logger.debug("AuthService.check_user")
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
            logger.info("User %s created", user_create.username)
            return ORJSONResponse(
                data=UserCreateSuccessSchema().model_dump(),
                status=201,
            )

        logger.info("User %s not created", user_create.username)
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
            token = encode_jwt_token(username=user.username, user_id=user.id)
            logger.info("User %s logged in", user.username)

            return ORJSONResponse(
                data=LoginSchemaSuccess(**token).model_dump(),
                status=200,
            )
        except UnAuthorized:
            logger.info("User %s not logged in", username)
            return ORJSONResponse(
                data=LoginSchemaFailed().model_dump(),
                status=401,
            )

    def refresh_token(
        self,
        refresh_token: str,
    ) -> Optional["ORJSONResponse"]:
        if not refresh_token:
            raise RefreshTokenRequired

        payload = decode_jwt_token(token=refresh_token)

        if not payload:
            raise InvalidToken
        user_id = payload.get("user_id")
        user = self.user_repository.get_user_by_id(user_id=user_id)

        if not user:
            raise UserDoesNotExist

        token = encode_jwt_token(username=user.username, user_id=user.id)
        if token:
            logger.info("User %s refreshed token", user.username)
            return ORJSONResponse(
                data=RefreshTokenSchemaSuccess(**token).model_dump(),
                status=200,
            )

        logger.info("User %s not refreshed token", user.username)
        return ORJSONResponse(
            data=RefreshTokenSchemaFailed().model_dump(),
            status=401,
        )
