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

from src.users.enums import CountryCodeEnum
from src.users.validations import validate_birth_date, validate_code, validate_phone


class PhoneNumberSchema(BaseModel):
    country_code: CountryCodeEnum
    number: str = Field(..., min_length=9, max_length=9)

    @model_serializer
    def serialize_model(self):
        return {
            "phone_number": f"{self.country_code.value}{self.number}",
        }

    @model_validator(mode="after")
    def validate_phone(self):
        if validate_phone(country_code=self.country_code.value, number=self.number):
            return self

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile creation phone schema",
            "title": "RegisterPhoneSchema",
            "example": {
                "country_code": "+48",
                "number": "510100100",
            },
        }
    )


class PhoneCodeSchema(BaseModel):
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


class SendCodeSchema(BaseModel):
    code: str
    token: str

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Send code schema",
            "title": "SendCodeSchema",
            "example": {
                "code": "1234",
                "token": "token",
            },
        }
    )
