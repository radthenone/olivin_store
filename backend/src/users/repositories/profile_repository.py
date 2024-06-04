import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from django.db import transaction

from src.users.interfaces import IProfileRepository
from src.users.models import Profile

if TYPE_CHECKING:
    from src.users.schemas import ProfileCreateSchema, ProfileUpdateSchema
    from src.users.types import ProfileType

logger = logging.getLogger(__name__)


class ProfileRepository(IProfileRepository):
    def __init__(self, repository, *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        return Profile.objects.get(user__id=user_id)

    @transaction.atomic
    def create_profile(
        self,
        profile_create: "ProfileCreateSchema",
        avatar: str,
        user_id: UUID,
    ):
        try:
            Profile.objects.create(
                **profile_create.model_dump(),
                avatar=avatar,
                user_id=user_id,
            )
        except Exception as e:
            logger.exception("create_profile: %s", e)
