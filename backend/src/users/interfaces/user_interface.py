from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, TypeVar
from uuid import UUID

from src.users.schemas import UserUpdateSchema

if TYPE_CHECKING:
    from src.users.models import User

UserType = TypeVar("UserType", bound=User)


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
        user_obj: "UserType",
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
        user: "UserType",
    ) -> bool:
        pass
