from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.users.schemas import ProfileCreateSchema, ProfileUpdateSchema
    from src.users.types import ProfileType, UserType


class IProfileRepository(ABC):
    @abstractmethod
    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        pass

    def create_profile(
        self,
        profile_create: "ProfileCreateSchema",
        avatar: str,
        user: "UserType",
    ) -> bool:
        pass
