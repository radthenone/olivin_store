import uuid
from datetime import timedelta
from logging import getLogger
from typing import TYPE_CHECKING, Optional, TypeVar, cast

from django.contrib.auth.hashers import check_password
from ninja_extra.exceptions import APIException

from src.auth.errors import InvalidToken, RefreshTokenRequired, UnAuthorized
from src.auth.schemas import (
    LoginSchemaFailed,
    LoginSchemaSuccess,
    RefreshTokenSchemaFailed,
    RefreshTokenSchemaSuccess,
    RegisterUserMailSchema,
    RegisterUserMailSchemaSuccess,
    UserCreateFailedSchema,
    UserCreateSchema,
    UserCreateSuccessSchema,
)
from src.auth.utils import decode_jwt_token, encode_jwt_token, get_backend_url
from src.common.responses import ORJSONResponse
from src.users.errors import (
    EmailAlreadyExists,
    UserDoesNotExist,
    UsernameAlreadyExists,
)

if TYPE_CHECKING:
    from src.data.handlers import ImageFileHandler
    from src.data.interfaces import (
        ICacheHandler,
        IFileHandler,
        IRegistrationEmailHandler,
    )
    from src.users.interfaces import IUserRepository
    from src.users.types import UserType

logger = getLogger(__name__)


class AuthService:
    def __init__(
        self,
        repository: "IUserRepository",
        cache_handler: "ICacheHandler",
        mail_handler: "IRegistrationEmailHandler",
        image_handler: "IFileHandler",
        *args,
        **kwargs,
    ):
        self.user_repository = repository
        self.cache = cache_handler
        self.mail = mail_handler
        self.image = cast("ImageFileHandler", image_handler)
        super().__init__(*args, **kwargs)

    def create_register_token(self, token: str, email: str) -> None:
        self.cache.set_value(
            key=token, value={"email": email}, expire=timedelta(minutes=30)
        )
        logger.info("Token %s created for 30 minutes registration", token)

    def get_register_token(self, token: str) -> Optional[dict]:
        value = self.cache.get_value(key=token)
        if value:
            logger.info("Token %s exists", token)
            return value
        logger.info("Token %s does not exist", token)
        return None

    @staticmethod
    def generate_register_token() -> str:
        token = str(uuid.uuid4())
        return token

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

    def check_user(self, user) -> None:
        logger.debug("AuthService.check_user")
        username = getattr(user, "username", None)
        email = getattr(user, "email", None)

        if username and self.user_repository.get_user_by_username(username=username):
            raise UsernameAlreadyExists

        if email and self.user_repository.get_user_by_email(email=email):
            raise EmailAlreadyExists

    def register_user_mail(
        self,
        token: str,
        user_register: "RegisterUserMailSchema",
    ) -> Optional["ORJSONResponse"]:
        if user_register.email:
            self.create_register_token(token, user_register.email)
            add_path = "/auth/register/mail/" + token
            register_url = get_backend_url(add_path=add_path)
            logger.info("Register token: %s created", token)
            image = self.image.get_image("register.webp")
            if self.mail.send_registration_email(
                to_email=user_register.email,
                context={
                    "url": register_url,
                    "image": image,
                },
            ):
                logger.info("Email sent to %s", user_register.email)
                return ORJSONResponse(
                    data=RegisterUserMailSchemaSuccess(url=register_url).model_dump(),
                    status=200,
                )
            else:
                logger.info("Mail not sent to %s", user_register.email)
                raise APIException("Mail not sent", code=400)
        logger.info(
            "Email does not exist",
        )
        raise APIException("Email does not exist", code=400)

    def register_user(
        self,
        token: str,
        user_create: "UserCreateSchema",
    ) -> Optional["ORJSONResponse"]:
        email = self.get_register_token(token=token)["email"]
        if email:
            user_create.email = email
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
