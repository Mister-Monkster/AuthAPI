from typing import Annotated
from fastapi import Depends

from Repositories.chat_repository import ChatRepository
from dependecies.session_depends import SessionDep
from Repositories.user_repository import UserRepository


async def get_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

RepositoryDep = Annotated[UserRepository, Depends(get_repository)]


async def get_chat_repository(session: SessionDep) -> ChatRepository:
    return ChatRepository(session)

ChatRepositoryDep = Annotated[ChatRepository, Depends(get_chat_repository)]
