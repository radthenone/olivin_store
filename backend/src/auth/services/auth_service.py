import uuid
from datetime import timedelta
from logging import getLogger
from typing import TYPE_CHECKING, Optional, cast

from django.contrib.auth.hashers import check_password
from django.db import transaction
from ninja_extra.exceptions import APIException

from src.auth import errors as auth_errors
from src.auth import schemas as auth_schemas
from src.auth.tasks import send_registration_email_task
from src.auth.utils import decode_jwt_token, encode_jwt_token, get_backend_url
from src.common.responses import ORJSONResponse
from src.common.schemas import MessageSchema
from src.data.managers.task_manager import TaskManager
from src.users import errors as users_errors
from src.users import schemas as users_schemas

if TYPE_CHECKING:
    from src.data.handlers import (  # unused import
        ImageFileHandler,
    )
    from src.data.interfaces import (
        ICacheHandler,
        IEventHandler,
        IFileHandler,
    )
    from src.users.services import ProfileService, UserService
    from src.users.types import UserType

task_manager = TaskManager(queue="tasks")

logger = getLogger(__name__)


class AuthService:
    def __init__(
        self,
        cache_handler: "ICacheHandler",
        event_handler: "IEventHandler",
        image_handler: "IFileHandler",
        user_service: "UserService",
        profile_service: "ProfileService",
        *args,
        **kwargs,
    ):
        self.cache = cache_handler
        self.event = event_handler
        self.image = cast("ImageFileHandler", image_handler)
        self.user_service = user_service
        self.profile_service = profile_service
        super().__init__(*args, **kwargs)

    def create_register_token(self, token: str, email: str) -> None:
        self.cache.set_value(
            key=token, value={"email": email}, expire=timedelta(minutes=30)
        )
        logger.info(
            "Token [green]%s[/] created for [blue]30[/] minutes registration",
            token,
            extra={"markup": True},
        )

    def get_register_token(self, token: str) -> Optional[dict]:
        value = self.cache.get_value(key=token)
        if value:
            logger.info(
                "Token [green]%s[/] exists",
                token,
                extra={"markup": True},
            )
            return value
        logger.info(
            "Token [green]%s[/] does not exist",
            token,
            extra={"markup": True},
        )
        raise auth_errors.TokenDoesNotExist

    @staticmethod
    def generate_register_token() -> str:
        token = str(uuid.uuid4())
        return token

    def authorized_user(
        self,
        username: str,
        password: str,
    ) -> Optional["UserType"]:
        user = self.user_service.get_user_by_username(username=username)
        if user is None:
            raise users_errors.UserDoesNotExist
        if not check_password(password, user.password):
            raise auth_errors.UnAuthorized
        logger.info(
            "User [blue]%s[/] authorized",
            user.username,
            extra={"markup": True},
        )
        return user

    def check_user(self, user) -> None:
        username = getattr(user, "username", None)
        email = getattr(user, "email", None)

        if username and self.user_service.get_user_by_username(username=username):
            raise users_errors.UsernameAlreadyExists

        if email and self.user_service.get_user_by_email(email=email):
            raise users_errors.EmailAlreadyExists

    @transaction.atomic
    def register_user_mail(
        self,
        user_register_mail_schema: "auth_schemas.RegisterUserMailSchema",
    ) -> Optional["auth_schemas.RegisterUrlSchema"]:
        token = self.generate_register_token()
        if user_register_mail_schema.email:
            self.create_register_token(token, user_register_mail_schema.email)
            add_path = "/auth/register/mail/" + token
            register_url = get_backend_url(add_path=add_path)
            logger.info("Register token: %s created", token)
            image = self.image.get_image("register.webp")
            transaction.on_commit(
                lambda: send_registration_email_task.apply_async(
                    kwargs={
                        "url": register_url,
                        "image": image,
                        "email": user_register_mail_schema.email,
                    },
                )
            )
            return auth_schemas.RegisterUrlSchema(url=register_url)
        logger.info(
            "Email [blue]%s[/] does not send",
            user_register_mail_schema.email,
            extra={"markup": True},
        )
        raise auth_errors.MailDoesNotSend

    @transaction.atomic
    def register_user(
        self,
        token: str,
        register_schema: "auth_schemas.RegisterSchema",
    ) -> Optional["auth_schemas.RegisterSuccessSchema"]:
        register_token = self.get_register_token(token=token)
        user_create_schema = users_schemas.UserCreateSchema(
            email=register_token.get("email"),
            **register_schema.model_dump(
                include={
                    "username",
                    "password",
                    "rewrite_password",
                    "first_name",
                    "last_name",
                }
            ),
        )

        self.check_user(user=user_create_schema)

        try:
            user_id = self.user_service.create_user(
                user_create=user_create_schema,
                timeout=1,
            )
            user_db = self.user_service.get_user_by_id(user_id=uuid.UUID(user_id))
            if not user_db:
                raise users_errors.UserCreateFailed

            profile_create_schema = users_schemas.ProfileCreateSchema(
                birth_date=register_schema.birth_date,
            )

            self.event.publish(
                event_name="user_created",
                event_data={
                    "user_id": user_id,
                    "profile_create_schema": profile_create_schema.model_dump(),
                },
            )
            logger.info("Publishing user_created event for user ID: %s", user_id)

            # Wait for profile creation to complete
            event_data = self.event.receive(
                "profile_created", timeout=2, with_subscription=True
            )
            if event_data and event_data.get("is_created"):
                profile_data = event_data.get("profile_data")
                profile_db = self.profile_service.get_profile_by_id(
                    profile_id=uuid.UUID(profile_data.get("id")),
                )
                if profile_db and user_db:
                    logger.info(
                        "User %s created successfully with profile %s",
                        user_db.to_dict(include=["id", "username", "email"]),
                        profile_db.to_dict(include=["id", "birth_date"]),
                        extra={"markup": True},
                    )
                    return auth_schemas.RegisterSuccessSchema()
            else:
                logger.info(
                    "Profile creation failed for user %s, deleting user",
                    user_db.username,
                )
                if self.profile_service.get_profile_by_user_id(
                    user_id=uuid.UUID(user_id)
                ):
                    self.profile_service.delete_profile(user_id=user_id)
                self.user_service.delete_user(user_id=user_id)
                raise users_errors.UserCreateFailed

        except APIException as error:
            logger.error("Error during user registration: %s", str(error))
            raise users_errors.UserCreateFailed

    def login_user(
        self,
        username: str,
        password: str,
    ) -> Optional["auth_schemas.LoginSchemaSuccess"]:
        try:
            user = self.authorized_user(username, password)
            token = encode_jwt_token(username=user.username, user_id=user.id)
            logger.info(
                "User [green]%s[/] logged in",
                user.username,
                extra={"markup": True},
            )
            return auth_schemas.LoginSchemaSuccess(**token)
        except auth_errors.UnAuthorized:
            logger.info("User %s not logged in", username)
            raise auth_errors.NotLoggedIn

    def refresh_token(
        self,
        refresh_token: str,
    ) -> Optional["auth_schemas.RefreshTokenSchemaSuccess"]:
        if not refresh_token:
            raise auth_errors.RefreshTokenRequired

        payload = decode_jwt_token(token=refresh_token)

        if not payload:
            raise auth_errors.InvalidToken
        user_id = payload.get("user_id")
        user = self.user_service.get_user_by_id(user_id=user_id)

        if not user:
            raise users_errors.UserDoesNotExist

        token = encode_jwt_token(username=user.username, user_id=user.id)
        if not token:
            raise auth_errors.InvalidToken
        return auth_schemas.RefreshTokenSchemaSuccess(**token)
