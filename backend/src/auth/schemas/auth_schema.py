from typing import Annotated

from ninja import Schema
from pydantic import (
    BeforeValidator,
    ConfigDict,
    model_validator,
)

from src.users.validations import (
    check_passwords_match,
    validate_email,
    validate_password,
    validate_username,
)


class LoginSchema(Schema):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(LoginSchema):
    pass


class PasswordsMatchSchema(Schema):
    password: Annotated[str, BeforeValidator(validate_password)]
    rewrite_password: Annotated[str, BeforeValidator(validate_password)]

    @model_validator(mode="after")
    def passwords_match(self) -> "PasswordsMatchSchema":
        if check_passwords_match(self.password, self.rewrite_password):
            return self


class UserCreateSchema(PasswordsMatchSchema):
    username: Annotated[str, BeforeValidator(validate_username)]
    email: Annotated[str, BeforeValidator(validate_email)]
    first_name: str
    last_name: str

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
                "email": "a@a.com",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        }
    )


class UserCreateSuccessSchema(Schema):
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


class UserCreateFailedSchema(Schema):
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
