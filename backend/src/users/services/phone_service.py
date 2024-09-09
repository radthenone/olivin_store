from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from django.conf import settings
from ninja_extra.exceptions import APIException

from src.common.responses import ORJSONResponse
from src.common.schemas import MessageSchema
from src.users import errors as profile_errors
from src.users import schemas as profile_schemas
from src.users.schemas import (
    PhoneCodeSchema,
    PhoneNumberSchema,
    ProfileCreateSchema,
    ProfileUpdateSchema,
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


class PhoneService:
    def __init__(
        self,
        repository: "IProfileRepository" = None,
        event_handler: "IEventHandler" = None,
        cache_handler: "ICacheHandler" = None,
        phone_handler: "IPhoneHandler" = None,
        *args,
        **kwargs,
    ):
        self.profile_repository = repository
        self.event = event_handler
        self.cache = cache_handler
        self.phone = phone_handler
        super().__init__(*args, **kwargs)

    def is_exists(self, user_id: UUID, phone_number: str) -> bool:
        if self.profile_repository.is_phone_exists(
            user_id=user_id, phone_number=phone_number
        ):
            return True
        return False

    def send_code(
        self,
        user_id: UUID,
        phone_schema: PhoneNumberSchema,
    ) -> bool:
        try:
            phone_number = phone_schema.model_dump().get("phone_number")
            if self.is_exists(user_id=user_id, phone_number=phone_number):
                raise profile_errors.PhoneAlreadyExists
            phone_token = self.phone.verify_number(
                number=phone_number,
                brand="Olivin Store verification code",
            )
            if not settings.DEBUG_ON:
                code = generate_code()
                self.cache.set_value(
                    key=phone_token,
                    value={
                        "code": code,
                    },
                )
            if phone_token:
                logger.info(
                    "Phone [blue]%s[/] sent with token: [blue]%s[/]",
                    phone_number,
                    phone_token,
                    extra={"markup": True},
                )
                return True

        except Exception as error:
            logger.exception(
                """Phone not sent with error: [red]%s[/]""",
                error,
                extra={"markup": True},
            )

        return False

    def get(
        self,
        user_id: UUID,
    ) -> Optional[str]:
        return self.profile_repository.get_phone(user_id=user_id)

    def create(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        if self.is_exists(user_id=user_id, phone_number=phone_number):
            raise profile_errors.PhoneAlreadyExists

        try:
            self.profile_repository.create_phone(
                user_id=user_id,
                phone_number=phone_number,
            )
            logger.info(
                "Phone [blue]%s[/] created successfully",
            )
            return True

        except Exception as error:
            logger.exception(
                """Phone not created with error: [red]%s[/]""",
                error,
                extra={"markup": True},
            )

        return False

    def verify_code(
        self,
        request_id: str,
        code: str,
        user_id: UUID,
    ) -> bool:
        try:
            is_verified = self.phone.verify_number_code(
                request_id=request_id,
                code=code,
            )
            if is_verified:
                logger.info(
                    "Phone [blue]%s[/] verified successfully",
                    user_id,
                    extra={"markup": True},
                )
                return True
        except Exception as error:
            logger.exception(
                """Phone not verified with error: [red]%s[/]""",
                error,
                extra={"markup": True},
            )

        return False

    def update(
        self,
        user_id: UUID,
        phone_number: str,
    ) -> bool:
        if self.is_exists(user_id=user_id, phone_number=phone_number):
            raise profile_errors.PhoneAlreadyExists

        try:
            self.profile_repository.update_phone(
                user_id=user_id,
                phone_number=phone_number,
            )
            logger.info(
                "Phone [blue]%s[/] updated successfully",
            )
            return True

        except Exception as error:
            logger.exception(
                """Phone not updated with error: [red]%s[/]""",
                error,
                extra={"markup": True},
            )

        return False

    def delete(
        self,
        user_id: UUID,
    ) -> bool:
        try:
            self.profile_repository.delete_phone(
                user_id=user_id,
            )
            logger.info(
                "Phone [blue]%s[/] deleted successfully",
            )
            return True

        except Exception as error:
            logger.exception(
                """Phone not deleted with error: [red]%s[/]""",
                error,
                extra={"markup": True},
            )

        return False
