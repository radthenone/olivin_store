from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    model_validator,
)

from src.auth.schemas import PasswordsMatchSchema
from src.users.validations import (
    check_passwords_match,
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


class UserCreateSchema(UserUpdateSchema, PasswordsMatchSchema):
    email: Annotated[str, BeforeValidator(validate_email)]

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["password", "email"],
            "properties": {
                "password": {
                    "type": "string",
                    "minLength": 8,
                },
                "rewrite_password": {
                    "type": "string",
                    "minLength": 8,
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
                "password": "password",
                "rewrite_password": "password",
                "username": "username",
                "email": "a@a.com",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        }
    )


class SuperUserCreateSchema(BaseModel):
    password: Annotated[str, BeforeValidator(validate_password)]
    email: Annotated[str, BeforeValidator(validate_email)]
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
