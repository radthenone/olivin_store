from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.users.schemas import ProfileCreateSchema, ProfileUpdateSchema
    from src.users.types import ProfileType


class IProfileRepository(ABC):
    @abstractmethod
    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional[ProfileType]:
        pass

    def create_profile(
        self,
        profile_create: "ProfileCreateSchema",
    ):
        pass

    @abstractmethod
    def update_profile(
        self,
        profile_obj: ProfileType,
        profile_update: "ProfileUpdateSchema",
    ):
        pass

    @abstractmethod
    def delete_profile(
        self,
        profile_obj: ProfileType,
    ):
        pass
