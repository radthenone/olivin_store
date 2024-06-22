import json
import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from django.db import IntegrityError

from src.users.interfaces import IProfileRepository
from src.users.models import Profile

if TYPE_CHECKING:
    from src.users.schemas import ProfileCreateSchema, ProfileUpdateSchema
    from src.users.types import ProfileType, UserType

logger = logging.getLogger(__name__)


class ProfileRepository(IProfileRepository):
    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        return Profile.objects.get(user__id=user_id)

    def create_profile(
        self,
        profile_create: "ProfileCreateSchema",
        avatar: str,
        user: "UserType",
    ) -> bool:
        profile_data = json.loads(profile_create.model_dump_json())
        profile_data.update({"avatar": avatar, "user": user})

        try:
            Profile.objects.create(**profile_data)
            logger.info("create_profile: %s", user.username)
            return True
        except IntegrityError as e:
            logger.exception("create_profile: %s", e)
            return False
