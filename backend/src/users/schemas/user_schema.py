from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
)
from pydantic.fields import Field

from src.common.schemas import (
    MessageSchema,
    PasswordsMatchSchema,
)
from src.users.validations import (
    validate_email,
    validate_password,
    validate_username,
)


class UserCreateSchema(PasswordsMatchSchema):
    username: Annotated[str, BeforeValidator(validate_username)]
    email: Annotated[str, BeforeValidator(validate_email)] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["password", "email", "rewrite_password", "username"],
            "properties": {
                "password": {
                    "type": "string",
                    "minLength": 8,
                    "format": "password",
                },
                "rewrite_password": {
                    "type": "string",
                    "minLength": 8,
                    "format": "password",
                },
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
                "email": {
                    "type": "string",
                    "format": "email",
                },
            },
            "description": "User create schema",
            "title": "User create schema",
            "example": {
                "password": "Password12345!",
                "rewrite_password": "Password12345!",
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        }
    )


class UserUpdateSchema(BaseModel):
    username: Annotated[str, BeforeValidator(validate_username)] = None
    email: Annotated[str, BeforeValidator(validate_email)] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 16,
                },
                "email": {
                    "type": "string",
                    "format": "email",
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
                "username": "new_username",
                "email": "new@new.com",
                "first_name": "new_first_name",
                "last_name": "new_last_name",
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


class PasswordUpdateSchema(PasswordsMatchSchema):
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


class EmailUpdateSchema(BaseModel):
    email: Annotated[
        str, Field(..., alias="new_email"), BeforeValidator(validate_email)
    ]
    old_email: Annotated[str, BeforeValidator(validate_email)]
    old_password: Annotated[str, BeforeValidator(validate_password)]

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
                "old_password": {
                    "type": "string",
                    "minLength": 8,
                },
            },
            "description": "Email change schema",
            "title": "Email change schema",
            "example": {
                "new_email": "b@b.com",
                "old_email": "a@a.com",
                "old_password": "Password12345!",
            },
        }
    )


class EmailUpdateErrorSchema(MessageSchema):
    message: str = "Error while updating email"

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Email update error schema",
            "title": "Email update error schema",
            "example": {
                "message": "Error while updating email",
            },
        }
    )


class EmailUpdateSuccessSchema(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Email update success schema",
            "title": "Email update success schema",
            "example": {
                "email": "a@a.com",
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        }
    )


class UserProfileSuccessSchema(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    birth_date: date
    phone: str

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Email update success schema",
            "title": "Email update success schema",
            "example": {
                "email": "a@a.com",
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
                "birth_date": "1990-01-01",
                "phone": "+48510100100",
            },
        }
    )


class UserProfileErrorSchema(BaseModel):
    message: str = "Error while updating profile"

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Email update error schema",
            "title": "Email update error schema",
            "example": {
                "message": "Error while updating profile",
            },
        }
    )


class UserSchema(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str

    model_config = ConfigDict(
        json_schema_extra={
            "description": "User get success schema",
            "title": "User get success schema",
            "example": {
                "id": "123e4567-e89b-12d3-a456-426655440000",
                "email": "a@a.com",
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        }
    )
