import json
import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from django.db import IntegrityError
from django.forms import model_to_dict

from src.users.interfaces import IProfileRepository
from src.users.models import Profile

if TYPE_CHECKING:
    from src.users.schemas import (
        CreatePhoneSchema,
        ProfileCreateSchema,
        ProfileUpdateSchema,
        RegisterPhoneSchema,
    )
    from src.users.types import ProfileType, UserType

logger = logging.getLogger(__name__)


class ProfileRepository(IProfileRepository):
    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        try:
            return Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            return None

    def get_profile_by_id(
        self,
        profile_id: UUID,
    ) -> Optional["ProfileType"]:
        try:
            return Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return None

    def create_profile(
        self,
        profile_create: "ProfileCreateSchema",
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        profile_data = profile_create.model_dump()
        profile_data.update({"user_id": user_id})

        try:
            profile_db = Profile(**profile_data)
            profile_db.save()
            logger.info("create_profile: %s", profile_db.user.email)
            return profile_db
        except IntegrityError as e:
            logger.exception("create_profile: %s", e)
            return None

    def update_profile(
        self,
        profile_update: "ProfileUpdateSchema",
        user_id: UUID,
        avatar: Optional[str] = None,
    ) -> bool:
        try:
            profile_update_data = json.loads(profile_update.model_dump_json())

            if avatar is not None:
                profile_update_data.update({"avatar": avatar})

            Profile.objects.filter(user__id=user_id).update(
                **profile_update_data,
            )
            logger.info("update_profile: %s", user_id)
            return True
        except Exception as e:
            logger.exception("update_profile: %s", e)
            return False

    def delete_profile(
        self,
        user_id: UUID,
    ) -> bool:
        try:
            Profile.objects.get(user__id=user_id).delete()
            logger.info("delete_profile: %s", user_id)
            return True
        except Exception as e:
            logger.exception("delete_profile: %s", e)
            return False

    def create_profile_phone(
        self,
        phone: "RegisterPhoneSchema",
        user_id: UUID,
    ) -> bool:
        try:
            profile = Profile.objects.get(user__id=user_id)
            setattr(profile, "phone", phone.number)
            profile.save()
            logger.info("create_profile_phone: %s", user_id)
            return True
        except Exception as e:
            logger.exception("create_profile_phone: %s", e)
            return False

    def exists_profile_phone(
        self,
        user_id: UUID,
        number: str,
    ) -> bool:
        return Profile.objects.filter(user__id=user_id, phone=number).exists()
