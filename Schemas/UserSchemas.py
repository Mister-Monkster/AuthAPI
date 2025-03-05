import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class SRegistration(BaseModel):
    email: str
    username: str
    phone: str
    password: str
    birth: Optional[datetime.date]
    city: Optional[str]
    street: Optional[str]
    home: Optional[str]
    flat: Optional[int]
    bio: Optional[str]

    @field_validator("password", mode="before")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Пароль слишком короткий')
        elif value.islower():
            raise ValueError('В пароле должна содержаться хотя бы одна заглавная буква')
        return value
