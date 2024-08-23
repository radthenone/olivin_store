import json
import time
import uuid
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from django.forms import model_to_dict
from ninja_extra.exceptions import APIException

from src.common.responses import ORJSONResponse
from src.common.schemas import MessageSchema
from src.users import errors as profile_errors
from src.users import schemas as profile_schemas
from src.users.errors import ProfileDoesNotExist, ProfileNotFound
from src.users.schemas import (
    CreatePhoneSchema,
    ProfileCreateSchema,
    ProfileUpdateSchema,
    RegisterPhoneSchema,
)
from src.users.tasks import create_profile_task, delete_profile_task
from src.users.utils import generate_code, get_task_result

if TYPE_CHECKING:
    from src.data.handlers import AvatarFileHandler  # unused import
    from src.data.interfaces import (
        ICacheHandler,
        IEventHandler,
        IFileHandler,
        IPhoneHandler,
    )
    from src.users.interfaces import IProfileRepository
    from src.users.types import ProfileType

import logging

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(
        self,
        repository: "IProfileRepository" = None,
        event_handler: "IEventHandler" = None,
        avatar_handler: "IFileHandler" = None,
        cache_handler: "ICacheHandler" = None,
        phone_handler: "IPhoneHandler" = None,
        *args,
        **kwargs,
    ):
        self.profile_repository = repository
        self.event = event_handler
        self.avatar = cast("AvatarFileHandler", avatar_handler)
        self.cache = cache_handler
        self.phone = phone_handler
        super().__init__(*args, **kwargs)

    def get_profile_by_id(
        self,
        profile_id: UUID,
    ) -> Optional["ProfileType"]:
        profile = self.profile_repository.get_profile_by_id(profile_id)
        return profile

    def get_profile_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional["ProfileType"]:
        profile = self.profile_repository.get_profile_by_user_id(user_id)
        return profile

    @staticmethod
    def create_profile(
        profile_create_schema: "ProfileCreateSchema",
        user_id: UUID,
        timeout: Optional[int] = None,
    ) -> Optional[str]:
        task = create_profile_task.delay(
            user_id=user_id,
            profile_create_data=profile_create_schema.model_dump(),
        )
        profile_id = task.get(timeout=timeout)
        if not profile_id:
            logger.error("Profile creation failed")
        logger.info(
            "Profile [green]%s[/] creation success",
            profile_id,
            extra={"markup": True},
        )
        return profile_id

    @staticmethod
    def delete_profile(
        user_id: str,
    ) -> bool:
        task = delete_profile_task.delay(
            user_id=user_id,
        )
        is_deleted = task.get()
        if not is_deleted:
            logger.error(
                "Profile [green]%s[/] deletion failed",
                user_id,
                extra={"markup": True},
            )
        logger.info(
            "Profile [green]%s[/] deletion success",
            user_id,
            extra={"markup": True},
        )
        return is_deleted

    def handle_user_created(self):
        self.event.subscribe("user_created")
        while True:
            event_data = self.event.receive("user_created")
            if event_data:
                logger.info(
                    "[green]%s[/] got data: [blue]%s[/]",
                    self.handle_user_updated.__name__,
                    event_data,
                    extra={"markup": True},
                )

                if event_data["user_id"] and event_data["profile_create_schema"]:
                    user_id = event_data["user_id"]
                    profile_create_schema = ProfileCreateSchema(
                        birth_date=event_data["profile_create_schema"]["birth_date"],
                    )
                    profile_id = self.create_profile(
                        profile_create_schema=profile_create_schema,
                        user_id=user_id,
                    )
                    profile_db = self.profile_repository.get_profile_by_id(
                        profile_id=UUID(profile_id),
                    )
                    is_created = bool(profile_db)
                    profile_data = (
                        profile_db.to_dict(include=["id", "birth_date"])
                        if profile_db
                        else {}
                    )

                    if profile_db:
                        logger.info(
                            "[bold green]Profile created for user: [yellow]%s[/][/]",
                            str(profile_db.user_id),
                            extra={"markup": True},
                        )
                    else:
                        logger.info(
                            "[bold red]Profile not created for user:[yellow]%s[/][/]",
                            user_id,
                            extra={"markup": True},
                        )

                    # Notify that the profile has been created
                    self.event.publish(
                        "profile_created",
                        {
                            "user_id": user_id,
                            "is_created": is_created,
                            "profile_data": profile_data,
                        },
                    )
                    logger.info(
                        "Publishing profile_created event for profile ID: %s",
                        profile_id,
                    )

    def handle_user_updated(self):
        self.event.subscribe("user_updated")
        while True:
            event_data = self.event.receive("user_updated")
            if event_data:
                if event_data["user_id"] and event_data["profile_update"]:
                    user_id = event_data["user_id"]
                    profile_update = event_data["profile_update"]

                    if self.profile_repository.update_profile(
                        profile_update=ProfileUpdateSchema(**profile_update),
                        user_id=user_id,
                    ):
                        is_updated = True
                    else:
                        is_updated = False

                    self.event.publish(
                        "profile_updated",
                        {"user_id": user_id, "is_updated": is_updated},
                    )

    def register_phone(
        self,
        phone: "RegisterPhoneSchema",
        user_id: UUID,
    ) -> Optional["ORJSONResponse"]:
        if self.profile_repository.exists_profile_phone(
            user_id=user_id,
            number=phone.number,
        ):
            return ORJSONResponse(
                data=MessageSchema(message="Phone number already exists").model_dump(),
                status=400,
            )
        try:
            code = generate_code()
            token = self.phone.verify_number(
                number=phone.number,
                brand="Olivin Store",
            )
            self.cache.set_value(
                key=token,
                value={
                    "code": code,
                    "user_id": str(user_id),
                },
            )
            return ORJSONResponse(
                data={"token": token, "code": code},
                status=200,
            )
        except Exception as e:
            logger.exception("create_phone_code: %s", e)
            raise APIException("Invalid phone number", code=400)

    def create_phone(
        self,
        phone: "CreatePhoneSchema",
        user_id: UUID,
    ) -> Optional["ORJSONResponse"]:
        if self.phone.verify_number_code(
            request_id=phone.token,
            code=phone.code,
            user_id=user_id,
        ):
            logger.info("create_phone: %s", phone)
            return ORJSONResponse(
                data=MessageSchema(
                    message="Phone number created successfully"
                ).model_dump(),
                status=200,
            )
        else:
            logger.exception("create_phone failed: %s", phone)
            raise APIException("Invalid verification code", code=400)

    def get_profile(self, user_id: UUID) -> Optional["profile_schemas.ProfileSchema"]:
        profile = self.profile_repository.get_profile_by_user_id(user_id=user_id)
        if not profile:
            raise profile_errors.ProfileNotFound
        return profile_schemas.ProfileSchema(
            **profile.to_dict(
                include=[
                    "birth_date",
                    "phone",
                ]
            )
        )
