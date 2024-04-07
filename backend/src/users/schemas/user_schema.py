from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
)

from src.auth.schemas import PasswordsMatchSchema
from src.common.schemas import (
    MessageSchema,
)
from src.users.validations import (
    validate_email,
    validate_password,
    validate_username,
)


class UserUpdateSchema(BaseModel):
    username: Annotated[str, BeforeValidator(validate_username)]
    first_name: str
    last_name: str

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 16,
                },
                "first_name": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 16,
                },
                "last_name": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 16,
                },
            },
            "description": "User update schema",
            "title": "User update schema",
            "example": {
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        }
    )


class SuperUserCreateSchema(BaseModel):
    password: str
    email: str
    is_staff: bool = True
    is_superuser: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["password", "email"],
            "properties": {
                "password": {
                    "type": "string",
                    "minLength": 8,
                },
                "email": {
                    "type": "string",
                    "format": "email",
                },
            },
            "description": "Superuser create schema",
            "title": "Superuser create schema",
            "example": {
                "password": "password",
                "email": "a@a.com",
            },
        }
    )


class SuperUserCreateSuccessSchema(MessageSchema):
    message: str = "Superuser created successfully"

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Superuser create success schema",
            "title": "Superuser create success schema",
            "example": {
                "message": "Superuser created successfully",
            },
        }
    )


class SuperUserCreateErrorSchema(MessageSchema):
    message: str = "Error while creating superuser"

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Superuser create error schema",
            "title": "Superuser create error schema",
            "example": {
                "message": "Error while creating superuser",
            },
        }
    )


class PasswordsChangeSchema(PasswordsMatchSchema):
    old_password: Annotated[str, BeforeValidator(validate_password)]

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "old_password": {
                    "type": "string",
                    "minLength": 8,
                },
                "password": {
                    "type": "string",
                    "minLength": 8,
                },
                "rewrite_password": {
                    "type": "string",
                    "minLength": 8,
                },
            },
            "description": "Password change schema",
            "title": "Password change schema",
            "example": {
                "password": "password",
                "rewrite_password": "password",
                "old_password": "password",
            },
        }
    )


class EmailChangeSchema(BaseModel):
    new_email: Annotated[str, BeforeValidator(validate_email)]
    old_email: Annotated[str, BeforeValidator(validate_email)]
    password: Annotated[str, BeforeValidator(validate_password)]

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "new_email": {
                    "type": "string",
                    "minLength": 8,
                },
                "old_email": {
                    "type": "string",
                    "minLength": 8,
                },
                "password": {
                    "type": "string",
                    "minLength": 8,
                },
            },
            "description": "Email change schema",
            "title": "Email change schema",
            "example": {
                "new_email": "new_email",
                "old_email": "old_email",
                "password": "password",
            },
        }
    )
