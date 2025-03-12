import datetime
from typing import Annotated, Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[pk]
    username: Mapped[str] = mapped_column(String(24), index=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(11), unique=True, index=True)
    birth: Mapped[Optional[datetime.date]] = mapped_column(nullable=True)
    city: Mapped[Optional[str]]
    street: Mapped[Optional[str]]
    home: Mapped[Optional[str]]
    flat: Mapped[Optional[int]]
    bio: Mapped[Optional[str]] = mapped_column(String(1024))
    refresh_token: Mapped[Optional[str]] = mapped_column(default='')
