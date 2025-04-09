from datetime import datetime

from pydantic import BaseModel, ConfigDict



class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    id: int
    text: str
    sending_date: datetime
    user_rel: UserResponse

    model_config = ConfigDict(from_attributes=True)


class ChatResponse(BaseModel):
    id: int
    user_1: int
    user_2: int
    messages_rel: list[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)

