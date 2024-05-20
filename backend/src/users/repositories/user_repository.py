import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from django.contrib.auth import get_user_model

from src.users.interfaces import IUserRepository

if TYPE_CHECKING:
    from src.auth.schemas import UserCreateSchema
    from src.users.schemas import SuperUserCreateSchema, UserUpdateSchema
    from src.users.types import UserType


logger = logging.getLogger(__name__)

User = get_user_model()


class UserRepository(IUserRepository):
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
        user_create: "UserCreateSchema",
    ) -> bool:
        try:
            user_db = User(
                email=user_create.email,
                password=user_create.password,
                username=user_create.username,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
            )

            setattr(user_db, "is_staff", False)
            setattr(user_db, "is_superuser", False)

            user_db.set_password(user_create.password)
            user_db.save()
            logger.info("User created successfully with email %s", user_create.email)
        except Exception as error:
            logger.error("Error while creating user %s", error)
            return False
        return True

    def create_superuser(
        self,
        user_super_create: "SuperUserCreateSchema",
    ) -> bool:
        try:
            user_db = User(
                email=user_super_create.email,
                password=user_super_create.password,
                is_staff=user_super_create.is_staff,
                is_superuser=user_super_create.is_superuser,
            )
            user_db.set_password(user_super_create.password)
            user_db.save()
            logger.info(
                "Superuser created successfully with email %s", user_super_create.email
            )
        except Exception as error:
            logger.error("Error while creating superuser %s", error)
            return False
        return True

    def update_user(
        self,
        user_obj: "UserType",
        user_update: "UserUpdateSchema",
    ) -> "UserType":
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user_obj, field, value)
        user_obj.save()
        return user_obj

    def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        try:
            User.objects.get(id=user_id).delete()
            logger.info("User deleted successfully with id %s", user_id)
        except Exception as error:
            logger.error("Error while deleting user %s", error)
            return False
        return True
