from pydantic import (
    BaseModel,
    ConfigDict,
)


class AvatarSchema(BaseModel):
    avatar: str

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Avatar schema",
            "title": "AvatarSchema",
            "example": {
                "avatar": "https://example.com/avatar.png",
            },
        },
    )
