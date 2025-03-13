from pydantic import BaseModel


class MessageSchema(BaseModel):
    ok: bool
    detail: str
