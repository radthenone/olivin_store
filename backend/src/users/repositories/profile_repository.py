from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.users.interfaces import IProfileRepository
from src.users.models import Profile

if TYPE_CHECKING:
    from src.users.schemas import ProfileCreateSchema, ProfileUpdateSchema
    from src.users.types import ProfileType


class ProfileRepository(IProfileRepository):
    def __init__(self, repository, *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        return Profile.objects.get(user__id=user_id)
