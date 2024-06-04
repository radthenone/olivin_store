from datetime import date
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
)

from src.common.schemas import MessageSchema, PasswordsMatchSchema
from src.users.schemas import ProfileCreateSchema
from src.users.validations import (
    validate_birth_date,
    validate_email,
    validate_password,
    validate_phone,
    validate_username,
)


class RegisterUserMailSchema(BaseModel):
    email: Annotated[str, BeforeValidator(validate_email)]

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["email"],
            "properties": {
                "email": {
                    "type": "string",
                },
            },
            "description": "RegisterUserMail schema",
            "title": "RegisterUserMail schema",
            "example": {
                "email": "a@a.com",
            },
        }
    )


class RegisterUserMailSchemaSuccess(BaseModel):
    url: str


class LoginSchema(BaseModel):
    username: Annotated[str, BeforeValidator(validate_username)]
    password: Annotated[str, BeforeValidator(validate_password)]

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["password", "username"],
            "properties": {
                "password": {
                    "type": "string",
                },
                "username": {
                    "type": "string",
                },
            },
            "description": "LoginPage schema",
            "title": "LoginPage schema",
            "example": {
                "username": "username",
                "password": "Password12345!",
            },
        }
    )


class LoginSchemaSuccess(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginSchemaFailed(MessageSchema):
    message: str = "Invalid credentials"


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RefreshTokenSchemaSuccess(LoginSchemaSuccess):
    pass


class RefreshTokenSchemaFailed(MessageSchema):
    message: str = "Invalid refresh token"


class RegisterSchema(PasswordsMatchSchema):
    username: Annotated[str, BeforeValidator(validate_username)]
    email: Annotated[str, BeforeValidator(validate_email)] = None
    first_name: str
    last_name: str
    birth_date: Annotated[Optional[date], BeforeValidator(validate_birth_date)] = None
    phone: Annotated[Optional[str], BeforeValidator(validate_phone)] = None

    model_config = ConfigDict(
        json_schema_extra={
            "required": [
                "password",
                "email",
                "rewrite_password",
                "username",
                "first_name",
                "last_name",
                "birth_date",
                "phone",
            ],
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
                "birth_date": {
                    "type": "string",
                    "format": "date",
                },
                "phone": {
                    "type": "string",
                    "format": "phone",
                },
            },
            "description": "Register schema",
            "title": "Register schema",
            "example": {
                "password": "Password12345!",
                "rewrite_password": "Password12345!",
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "a@a.com",
                "birth_date": "1990-01-01",
                "phone": "+48510100100",
            },
        }
    )


class UserCreateSchema(PasswordsMatchSchema):
    username: Annotated[str, BeforeValidator(validate_username)]
    email: Annotated[str, BeforeValidator(validate_email)] = None
    first_name: str
    last_name: str
    profiles: ProfileCreateSchema

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


class UserCreateSuccessSchema(BaseModel):
    message: str = "User created successfully"

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["message"],
            "properties": {
                "message": {
                    "type": "string",
                },
            },
            "description": "User create success schema",
            "title": "User create success schema",
            "example": {
                "message": "User created successfully",
            },
        }
    )


class UserCreateFailedSchema(BaseModel):
    message: str = "User creation failed"

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["message"],
            "properties": {
                "message": {
                    "type": "string",
                },
            },
            "description": "User create failed schema",
            "title": "User create failed schema",
            "example": {
                "message": "User creation failed",
            },
        }
    )
