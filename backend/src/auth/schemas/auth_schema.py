from typing import Annotated

from pydantic import (
    BaseModel,
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


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class PasswordsMatchSchema(BaseModel):
    password: Annotated[str, BeforeValidator(validate_password)]
    rewrite_password: Annotated[str, BeforeValidator(validate_password)]

    @model_validator(mode="after")
    def passwords_match(self) -> "PasswordsMatchSchema":
        if check_passwords_match(self.password, self.rewrite_password):
            return self


class UserCreateSchema(BaseModel, PasswordsMatchSchema):
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
