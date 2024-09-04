from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.users.schemas import (
        PhoneCodeSchema,
        PhoneNumberSchema,
        ProfileCreateSchema,
        ProfileUpdateSchema,
    )
    from src.users.types import ProfileType, UserType


class IProfileRepository(ABC):
    @abstractmethod
    def is_profile_exists(self, user_id: UUID) -> bool:
        pass

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
    ) -> bool:
        pass

    @abstractmethod
    def delete_profile(
        self,
        user_id: UUID,
    ) -> bool:
        pass

    @abstractmethod
    def is_phone_exists(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        pass

    @abstractmethod
    def get_phone(
        self,
        user_id: UUID,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def create_phone(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        pass

    @abstractmethod
    def update_phone(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        pass

    @abstractmethod
    def delete_phone(
        self,
        user_id: UUID,
    ) -> bool:
        pass
