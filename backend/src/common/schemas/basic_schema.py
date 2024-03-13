from pydantic import BaseModel


class CreatedAtSchema(BaseModel):
    created_at: str


class UpdatedAtSchema(BaseModel):
    updated_at: str


class MessageSchema(BaseModel):
    message: str
