from datetime import date
from typing import Annotated, ClassVar, Optional

from pydantic import BaseModel, BeforeValidator, HttpUrl
from pydantic.config import ConfigDict

from src.users.validations import validate_birth_date, validate_phone


class ProfileCreateSchema(BaseModel):
    birth_date: Annotated[Optional[date], BeforeValidator(validate_birth_date)] = None
    avatar: Optional[HttpUrl] = None
    phone: Annotated[Optional[str], BeforeValidator(validate_phone)] = None

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile creation schema",
            "title": "ProfileCreate",
            "example": {
                "birth_date": "1990-01-01",
                "avatar": "http://example.com/path/to/avatar.jpg",
                "phone": "+48510100100",
            },
        }
    )


class ProfileUpdateSchema(BaseModel):
    birth_date: Annotated[Optional[date], BeforeValidator(validate_birth_date)] = None
    avatar: Optional[HttpUrl] = None
    phone: Annotated[Optional[str], BeforeValidator(validate_phone)] = None

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Profile update schema",
            "title": "ProfileUpdate",
            "example": {
                "birth_date": "1990-02-02",
                "avatar": "http://example.com/path/to/avatar2.jpg",
                "phone": "+48510100100",
            },
        }
    )
