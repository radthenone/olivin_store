from pydantic import BaseModel, ConfigDict


class CreatedAtSchema(BaseModel):
    created_at: str


class UpdatedAtSchema(BaseModel):
    updated_at: str


class MessageSchema(BaseModel):
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
