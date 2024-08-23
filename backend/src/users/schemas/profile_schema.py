from datetime import date
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    HttpUrl,
    field_serializer,
    model_serializer,
    model_validator,
)
from pydantic.fields import Field

from src.users.enums import CountryEnum
from src.users.validations import validate_birth_date, validate_code, validate_phone


class RegisterPhoneSchema(BaseModel):
    country: CountryEnum
    number: str = Field(..., min_length=9, max_length=9)

    @model_serializer
    def serialize_model(self):
        return {
            "phone": f"{self.country.name}{self.number}",
        }

    @model_validator(mode="after")
    def validate_phone(self):
        if validate_phone(country_code=self.country.name, number=self.number):
            return self

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile creation phone schema",
            "title": "RegisterPhoneSchema",
            "example": {
                "country": "POLAND",
                "number": "510100100",
            },
        }
    )


class CreatePhoneSchema(BaseModel):
    token: str
    code: Annotated[str, BeforeValidator(validate_code)]

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile code schema",
            "title": "CreatePhoneSchema",
            "example": {
                "token": "token",
                "code": "1234",
            },
        }
    )


class ProfileCreateSchema(BaseModel):
    birth_date: Annotated[Optional[str], BeforeValidator(validate_birth_date)] = None

    model_config = ConfigDict(
        strict=True,
        json_schema_extra={
            "description": "Profile creation schema",
            "title": "ProfileCreate",
            "example": {
                "birth_date": "1990-01-01",
            },
        },
    )


class ProfileUpdateSchema(BaseModel):
    birth_date: Annotated[Optional[date], BeforeValidator(validate_birth_date)] = None

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile update schema",
            "title": "ProfileUpdate",
            "example": {
                "birth_date": "1990-02-02",
            },
        }
    )


class ProfileSchema(BaseModel):
    birth_date: Optional[date]
    phone: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile schema",
            "title": "Profile",
            "example": {
                "birth_date": "1990-01-01",
                "phone": "+48510100100",
            },
        }
    )
