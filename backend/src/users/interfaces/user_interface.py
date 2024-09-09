from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.users import schemas as user_schemas
    from src.users.types import UserType


class IUserRepository(ABC):
    @abstractmethod
    def is_user_exists(
        self,
        user_id: UUID,
    ) -> bool:
        pass

    @abstractmethod
    def is_superuser_exists(self) -> bool:
        pass

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
        user_create_schema: "user_schemas.UserCreateSchema",
    ) -> Optional["UserType"]:
        pass

    @abstractmethod
    def create_superuser(
        self,
        super_user_create_schema: "user_schemas.SuperUserCreateSchema",
    ) -> Optional["UserType"]:
        pass

    @abstractmethod
    def update_user(
        self,
        user_id: UUID,
        user_update: "user_schemas.UserUpdateSchema",
    ) -> Optional["UserType"]:
        pass

    @abstractmethod
    def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        pass
