from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.users.schemas import (
        CreatePhoneSchema,
        ProfileCreateSchema,
        ProfileUpdateSchema,
        RegisterPhoneSchema,
    )
    from src.users.types import ProfileType, UserType


class IProfileRepository(ABC):
    @abstractmethod
    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        pass

    @abstractmethod
    def get_profile_by_id(
        self,
        profile_id: UUID,
    ) -> Optional["ProfileType"]:
        pass

    @abstractmethod
    def create_profile(
        self,
        profile_create: "ProfileCreateSchema",
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        pass

    @abstractmethod
    def update_profile(
        self,
        user_id: UUID,
        profile_update: "ProfileUpdateSchema",
        avatar: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def delete_profile(
        self,
        user_id: UUID,
    ) -> bool:
        pass

    @abstractmethod
    def create_profile_phone(
        self,
        phone: "RegisterPhoneSchema",
        user_id: UUID,
    ) -> bool:
        pass

    @abstractmethod
    def exists_profile_phone(
        self,
        user_id: UUID,
        number: str,
    ) -> bool:
        pass
