import datetime
from typing import Annotated, Optional

from sqlalchemy import String, UniqueConstraint, ForeignKey, text, CheckConstraint, Index, func
from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE( 'utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE( 'utc', now())"),
                                                        onupdate=datetime.datetime.utcnow, )]


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = 'users'

    __table_args__ = (
        UniqueConstraint('google_sub', 'email', name='uq_users_google_sub_email'),
    )

    id: Mapped[pk]
    username: Mapped[str] = mapped_column(String(24), index=True)
    password: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(11), unique=True, index=True)
    birth: Mapped[Optional[datetime.date]] = mapped_column(nullable=True)
    city: Mapped[Optional[str]]
    street: Mapped[Optional[str]]
    home: Mapped[Optional[str]]
    flat: Mapped[Optional[str]]
    bio: Mapped[Optional[str]] = mapped_column(String(1024))
    is_verificate: Mapped[bool] = mapped_column(default=False)
    google_sub: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True, server_default=None)
    chats_as_user1: Mapped[list['ChatModel']] = relationship(
        back_populates="user1_rel",
        foreign_keys="ChatModel.user_1"
    )
    chats_as_user2: Mapped[list['ChatModel']] = relationship(
        back_populates="user2_rel",
        foreign_keys="ChatModel.user_2"
    )
    user_messages_rel: Mapped[list['MessageModel']] = relationship(back_populates='user_rel')


class ChatModel(Base):
    __tablename__ = 'chats'

    id: Mapped[pk]
    messages_rel: Mapped[list['MessageModel']] = relationship(back_populates='chat_rel')
    user_1: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), index=True)
    user_2: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), index=True)
    user1_rel: Mapped['UserModel'] = relationship(back_populates="chats_as_user1", foreign_keys=[user_1])
    user2_rel: Mapped['UserModel'] = relationship(back_populates="chats_as_user2", foreign_keys=[user_2])

    __table_args__ = (
        UniqueConstraint('user_1', 'user_2', name='uq_chat_users'),
        Index('ix_chat_users_unique',
              func.least(user_1, user_2),
              func.greatest(user_1, user_2),
              unique=True),
        CheckConstraint('user_1 != user_2', name='check_no_self_chat'),
    )


class MessageModel(Base):
    __tablename__ = 'messages'

    id: Mapped[pk]
    chat_rel: Mapped['ChatModel'] = relationship(back_populates='messages_rel')
    user_rel: Mapped['UserModel'] = relationship(back_populates='user_messages_rel')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete="CASCADE"))
    text: Mapped[str]
    sending_date: Mapped[created_at]
    updated_at: Mapped[updated_at]
