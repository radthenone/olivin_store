from ninja.schema import Schema
from pydantic import ConfigDict


class CreatedAtSchema(Schema):
    created_at: str


class UpdatedAtSchema(Schema):
    updated_at: str


class MessageSchema(Schema):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "required": ["message"],
            "properties": {
                "message": {
                    "type": "string",
                },
            },
        }
    )
