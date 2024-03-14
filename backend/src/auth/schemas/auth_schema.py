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
