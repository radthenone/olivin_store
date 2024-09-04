import json
import logging
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from django.db import IntegrityError, transaction

from src.users.interfaces import IProfileRepository
from src.users.models import Profile

if TYPE_CHECKING:
    from src.users.schemas import (
        PhoneCodeSchema,
        PhoneNumberSchema,
        ProfileCreateSchema,
        ProfileUpdateSchema,
    )
    from src.users.types import ProfileType, UserType

logger = logging.getLogger(__name__)


class ProfileRepository(IProfileRepository):
    def is_profile_exists(self, user_id: UUID) -> bool:
        return Profile.objects.filter(user__id=user_id).exists()

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
        user_id: UUID,
        profile_create: "ProfileCreateSchema",
    ) -> Optional["ProfileType"]:
        profile_data = profile_create.model_dump(exclude_none=True)
        profile_data.update({"user_id": user_id})

        try:
            profile_db = Profile(**profile_data)
            profile_db.save()
            logger.info(
                "Profile created for user email: [blue]%s[/]",
                profile_db.user.email,
                extra={"markup": True},
            )
            return profile_db
        except IntegrityError as error:
            logger.exception(
                "Profile not created with error: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return None

    def update_profile(
        self,
        user_id: UUID,
        profile_update: "ProfileUpdateSchema",
    ) -> bool:
        try:
            with transaction.atomic():
                profile_db = self.get_profile_by_user_id(user_id=user_id)
                for field, value in profile_update.model_dump(
                    exclude_unset=True
                ).items():
                    setattr(profile_db, field, value)
                profile_db.save()
            logger.info(
                "Profile updated for user [blue]%s[/]",
                profile_db.user.email,
                extra={"markup": True},
            )
            return True
        except Exception as error:
            logger.exception(
                "Error while updating profile: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return False

    def delete_profile(
        self,
        user_id: UUID,
    ) -> bool:
        try:
            profile_db = self.get_profile_by_user_id(user_id=user_id)
            profile_db_email = profile_db.user.email
            profile_db.delete()
            logger.info(
                "Profile deleted for user email: [blue]%s[/]",
                profile_db_email,
                extra={"markup": True},
            )
            return True
        except Exception as error:
            logger.exception(
                "Error while deleting profile: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return False

    def is_phone_exists(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        return Profile.objects.filter(user__id=user_id, phone=phone_number).exists()

    def get_phone(
        self,
        user_id: UUID,
    ) -> Optional[str]:
        try:
            profile_db = self.get_profile_by_user_id(user_id=user_id)
            return profile_db.phone
        except Profile.DoesNotExist:
            return None

    def create_phone(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        try:
            profile_db = self.get_profile_by_user_id(user_id=user_id)
            if profile_db.phone is not None:
                raise Exception("Phone already exists")
            setattr(profile_db, "phone", phone_number)
            profile_db.save()
            logger.info(
                "Profile phone created for user [blue]%s[/] with phone [blue]%s[/]",
                profile_db.user.email,
                profile_db.phone,
                extra={"markup": True},
            )
            return True
        except Exception as error:
            logger.exception(
                "Profile phone not created with error: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return False

    def update_phone(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        try:
            profile_db = self.get_profile_by_user_id(user_id=user_id)
            if profile_db.phone == phone_number:
                raise Exception(f"This phone {phone_number} number already exists")
            if profile_db.phone is None:
                raise Exception("Phone does not exist, please create it first")
            setattr(profile_db, "phone", phone_number)
            profile_db.save()
            logger.info(
                "Profile phone updated for user [blue]%s[/], with new phone [blue]%s[/]",
                profile_db.user.email,
                profile_db.phone,
                extra={"markup": True},
            )
            return True
        except Exception as error:
            logger.exception(
                "Profile phone not updated with error: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return False

    def delete_phone(
        self,
        user_id: UUID,
    ) -> bool:
        try:
            profile_db = self.get_profile_by_user_id(user_id=user_id)
            if profile_db.phone is None:
                raise Exception("Phone does not exist")
            profile_delete_phone = profile_db.phone
            setattr(profile_db, "phone", None)
            profile_db.save()

            logger.info(
                "Profile phone: [blue]%s[/] deleted",
                profile_delete_phone,
                extra={"markup": True},
            )
            return True
        except Exception as error:
            logger.exception(
                "Profile phone not deleted with error: [red]%s[/]",
                error,
                extra={"markup": True},
            )
            return False
