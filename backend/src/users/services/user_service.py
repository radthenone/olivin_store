from typing import Optional
from uuid import UUID

from django.forms.models import model_to_dict
from ninja_extra.exceptions import APIException

from src.auth.utils import check_password, hash_password
from src.common.responses import ORJSONResponse
from src.users.errors import EmailAlreadyExists, WrongPassword
from src.users.schemas import (
    EmailUpdateErrorSchema,
    EmailUpdateSchema,
    EmailUpdateSuccessSchema,
    SuperUserCreateErrorSchema,
    SuperUserCreateSchema,
    SuperUserCreateSuccessSchema,
    UserUpdateSchema,
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

    def change_email(
        self,
        email_update: "EmailUpdateSchema",
        user_id: UUID,
    ) -> Optional["ORJSONResponse"]:
        user_obj = self.user_repository.get_user_by_id(user_id=user_id)
        if not check_password(email_update.old_password, user_obj.password):
            raise WrongPassword

        if email_update.email == user_obj.email:
            raise APIException(
                detail="You already have this email",
                code=400,
            )

        if email_update.old_email != user_obj.email:
            raise APIException(
                detail="Wrong old email",
                code=400,
            )

        user_data = self.user_repository.update_user(
            user_obj=user_obj,
            user_update=UserUpdateSchema(
                email=email_update.email,
                username=user_obj.username,
                first_name=user_obj.first_name,
                last_name=user_obj.last_name,
            ),
        )
        if user_data:
            return ORJSONResponse(
                data=EmailUpdateSuccessSchema(
                    **model_to_dict(
                        user_data,
                        fields=[
                            "email",
                            "username",
                            "first_name",
                            "last_name",
                        ],
                    )
                ).model_dump(),
                status=200,
            )
        return ORJSONResponse(
            data=EmailUpdateErrorSchema().model_dump(),
            status=400,
        )
