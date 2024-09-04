from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from ninja_extra.exceptions import APIException

from src.auth.utils import check_password
from src.users import errors as user_errors
from src.users import schemas as user_schemas
from src.users.tasks import create_user_task, delete_user_task

if TYPE_CHECKING:
    from src.data.handlers import AvatarFileHandler  # unused import
    from src.data.interfaces import (
        ICacheHandler,
        IEventHandler,
        IFileHandler,
    )
    from src.users.interfaces import IUserRepository
    from src.users.types import UserType


class UserService:
    def __init__(
        self,
        repository: "IUserRepository" = None,
        avatar_handler: "IFileHandler" = None,
        event_handler: "IEventHandler" = None,
        cache_handler: "ICacheHandler" = None,
        *args,
        **kwargs,
    ):
        self.user_repository = repository
        self.event = event_handler
        self.cache = cache_handler
        self.avatar = cast("AvatarFileHandler", avatar_handler)
        super().__init__(*args, **kwargs)

    def is_superuser_exists(self) -> bool:
        return self.user_repository.is_superuser_exists()

    def get_user_by_id(
        self,
        user_id: UUID,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_id(user_id)
        return user

    def get_user_by_email(
        self,
        email: str,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_email(email)
        return user

    def get_user_by_username(
        self,
        username: str,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_username(username)
        return user

    @staticmethod
    def create_user(
        user_create: "user_schemas.UserCreateSchema",
        timeout: Optional[int] = None,
    ) -> Optional[str]:
        task = create_user_task.delay(user_create=user_create.model_dump())
        user_id = task.get(timeout=timeout)
        if user_id:
            return user_id

        return None

    @staticmethod
    def delete_user(user_id: str) -> bool:
        task = delete_user_task.delay(user_id=user_id)
        return task.get()

    def create_superuser(
        self,
        super_user_create_schema: "user_schemas.SuperUserCreateSchema",
    ) -> Optional["UserType"]:
        if self.user_repository.get_user_by_email(
            email=super_user_create_schema.email,
        ):
            raise user_errors.EmailAlreadyExists

        try:
            super_user = self.user_repository.create_superuser(
                super_user_create_schema=super_user_create_schema,
            )
            return super_user

        except APIException:
            raise user_errors.SuperUserCreateFailed

    def get_user(self, user_id: UUID) -> Optional["user_schemas.UserSchema"]:
        user = self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise user_errors.UserNotFound
        return user_schemas.UserSchema(
            **user.to_dict(
                include=[
                    "id",
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                ]
            )
        )

    def change_email(
        self,
        email_update_schema: "user_schemas.EmailUpdateSchema",
        user_id: UUID,
    ) -> Optional["user_schemas.EmailUpdateSuccessSchema"]:
        user_db = self.user_repository.get_user_by_id(user_id=user_id)
        if not (
            check_password(email_update_schema.old_password, user_db.password)
            and email_update_schema.old_email == user_db.email
            and email_update_schema.email != user_db.email
        ):
            raise user_errors.WrongOldEmail

        user_updated_db = self.user_repository.update_user(
            user_db=user_db,
            user_update=user_schemas.UserUpdateSchema(
                email=email_update_schema.email,
            ),
        )
        if user_updated_db:
            return user_schemas.EmailUpdateSuccessSchema(
                **user_updated_db.to_dict(
                    include=["email", "username", "first_name", "last_name"]
                )
            )

        raise user_errors.EmailUpdateFailed

    # TODO update_user to create
    def update_user(
        self,
        user_id: UUID,
        user_update: "user_schemas.UserUpdateSchema",
        profile_update: "user_schemas.ProfileUpdateSchema",
    ):
        try:
            user_db = self.user_repository.get_user_by_id(user_id=user_id)
            user = self.user_repository.update_user(
                user_db=user_db,
                user_update=user_update,
            )
            if user:
                self.event.publish(
                    event_name="user_updated",
                    event_data={
                        "user_id": user_id,
                        "profile_update": profile_update.model_dump(),
                    },
                )

        except APIException:
            raise user_errors.UserUpdateFailed
