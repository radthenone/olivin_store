import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import transaction

from src.users.interfaces import IUserRepository

if TYPE_CHECKING:
    from src.users import schemas as user_schemas
    from src.users.types import UserType

logger = logging.getLogger(__name__)

User = get_user_model()


class UserRepository(IUserRepository):
    def is_user_exists(
        self,
        user_id: UUID,
    ) -> bool:
        return User.objects.filter(user_id=user_id).exists()

    def is_superuser_exists(self) -> bool:
        return User.objects.filter(is_superuser=True).exists()

    def get_user_by_id(
        self,
        user_id: UUID,
    ) -> Optional["UserType"]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get_user_by_email(
        self,
        email: str,
    ) -> Optional["UserType"]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user_by_username(
        self,
        username: str,
    ) -> Optional["UserType"]:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def create_user(
        self,
        user_create_schema: "user_schemas.UserCreateSchema",
    ) -> Optional["UserType"]:
        try:
            user_db = User(**user_create_schema.model_dump(exclude_none=True))

            setattr(user_db, "is_staff", False)
            setattr(user_db, "is_superuser", False)

            user_db.set_password(user_create_schema.password)
            user_db.save()
            logger.info(
                "User created successfully with email [blue]%s[/]",
                user_db.email,
                extra={"markup": True},
            )
            return user_db

        except Exception as error:
            logger.error("Error while creating user %s", error)
            return None

    def create_superuser(
        self,
        super_user_create_schema: "user_schemas.SuperUserCreateSchema",
    ) -> Optional["UserType"]:
        try:
            user_db = User(**super_user_create_schema.model_dump(exclude_none=True))
            user_db.set_password(super_user_create_schema.password)
            user_db.save()
            logger.info(
                "[green]Superuser created successfully with email [blue]%s[/][/]",
                user_db.email,
                extra={"markup": True},
            )
            return user_db
        except Exception as error:
            logger.error(
                "[red]Error while creating superuser [red bold]%s[/][/]",
                error,
                extra={"markup": True},
            )
            return None

    def update_user(
        self,
        user_id: UUID,
        user_update: "user_schemas.UserUpdateSchema",
    ) -> Optional["UserType"]:
        try:
            with transaction.atomic():
                user_db = self.get_user_by_id(user_id=user_id)
                for field, value in user_update.model_dump(exclude_unset=True).items():
                    setattr(user_db, field, value)
                user_db.save()
                logger.info(
                    "User updated successfully with email [blue]%s[/]",
                    user_db.email,
                    extra={"markup": True},
                )

                return user_db
        except Exception as error:
            logger.exception(
                "Error while updating user with error: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return None

    def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        try:
            user = User.objects.get(id=user_id)
            deleted_email = user.email
            user.delete()
            logger.info(
                "User deleted successfully with email [blue]%s[/]",
                deleted_email,
                extra={"markup": True},
            )
            return True
        except Exception as error:
            logger.error(
                "Error while deleting user error: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return False
