import datetime
import re
from typing import Optional, Any

from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Self

from pydantic import BaseModel, field_validator, ConfigDict, EmailStr


class SLogin(BaseModel):
    login: str = ''
    password: str = ''


class SProfile(BaseModel):
    username: str
    bio: Optional[str]
    is_verificate: bool

    model_config = ConfigDict(from_attributes=True)

class SAuth(BaseModel):
    email: EmailStr
    username: str
    phone: str
    birth: Optional[datetime.date]
    city: Optional[str]
    street: Optional[str]
    home: Optional[str]
    flat: Optional[int]
    bio: Optional[str]
    is_verificate: Optional[bool]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('phone', mode="before")
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError('Номер не может содержать буквы')
        return value


class SRegistration(BaseModel):
    email: EmailStr = ''
    password: str = ''
    username: str = ''
    phone: str = ''
    birth: Optional[datetime.date] = datetime.date(year=2000, month=1, day=1)
    city: Optional[str] = ''
    street: Optional[str] = ''
    home: Optional[str] = ''
    flat: Optional[str] = ''
    bio: Optional[str] = ''

    model_config = ConfigDict(from_attributes=True)

    @field_validator("flat", mode="before")
    def validate_flat(cls, value):
        if value:
            if not value.isdigit:
                raise ValueError('В поле "квартира" могут быть только цифры.')

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



class  SPasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

    @field_validator('confirm_new_password')
    def validate(cls, value, info: ValidationInfo):
        if value == info.data['new_password'] and value != info.data['old_password']:
            return value
        else:
            raise ValueError('Новый пароль не совпадает с полем проверки пароля.')




