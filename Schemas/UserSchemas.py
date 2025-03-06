import datetime
from typing import Optional, Any
from typing_extensions import Self
import re

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

    @field_validator('phone', mode="before")
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError('Номер не может содержать буквы')
        return value

    @field_validator('email', mode="before")
    def validate_email(cls, value):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if re.match(pattern, value) is not None:
            return value
        else:
            raise ValueError('Данная электронная почта невалидная')


