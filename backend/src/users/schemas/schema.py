from pydantic import ConfigDict

from src.users.schemas.profile_schema import ProfileUpdateSchema
from src.users.schemas.user_schema import UserUpdateSchema


class UserProfileUpdateSchema(UserUpdateSchema, ProfileUpdateSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "User and profile update schema",
            "title": "UserProfileUpdateSchema",
            "example": {
                "username": "new_username",
                "first_name": "new_first_name",
                "last_name": "new_last_name",
                "birth_date": "1990-02-02",
                "phone": "+48510100100",
            },
        }
    )
