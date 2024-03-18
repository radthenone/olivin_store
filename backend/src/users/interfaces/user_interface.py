from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.users.schemas import SuperUserCreateSchema, UserCreateSchema, UserUpdateSchema
from src.users.types import UserType


class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(
        self,
        user_id: UUID,
    ) -> Optional["UserType"]:
        pass

    @abstractmethod
    def get_user_by_email(
        self,
        email: str,
    ) -> Optional["UserType"]:
        pass

    @abstractmethod
    def get_user_by_username(
        self,
        username: str,
    ) -> Optional["UserType"]:
        pass

    @abstractmethod
    def create_user(
        self,
        user_create: UserCreateSchema,
    ) -> bool:
        pass

    @abstractmethod
    def create_superuser(
        self,
        user_super_create: SuperUserCreateSchema,
    ) -> bool:
        pass

    @abstractmethod
    def update_user(
        self,
        user_obj: "UserType",
        user_update: UserUpdateSchema,
    ):
        pass

    @abstractmethod
    def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        pass
