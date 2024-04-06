from typing import Optional

from src.common.responses import ORJSONResponse
from src.users.errors import EmailAlreadyExists
from src.users.schemas import (
    SuperUserCreateErrorSchema,
    SuperUserCreateSchema,
    SuperUserCreateSuccessSchema,
)


class UserService:
    def __init__(self, repository, *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def create_superuser(
        self,
        user_super_create: "SuperUserCreateSchema",
    ) -> Optional["ORJSONResponse"]:
        if self.user_repository.get_user_by_email(
            email=user_super_create.email,
        ):
            raise EmailAlreadyExists

        if self.user_repository.create_superuser(
            user_super_create=user_super_create,
        ):
            return ORJSONResponse(
                data=SuperUserCreateSuccessSchema().model_dump(),
                status=201,
            )

        return ORJSONResponse(
            data=SuperUserCreateErrorSchema().model_dump(),
            status=400,
        )
