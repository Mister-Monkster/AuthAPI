from typing import Annotated
from fastapi import Depends

from Services.chat_service import ChatService
from Services.user_service import UserService
from Services.oauth2_service import Oauth2Service
from Services.email_service import EmailService
from dependecies.repository_depends import RepositoryDep, ChatRepositoryDep
from dependecies.session_depends import RedisDep


async def get_userservice(repository: RepositoryDep) -> UserService:
    return UserService(repository)

user_service = Annotated[UserService, Depends(get_userservice)]


async def get_service(repository: RepositoryDep) -> Oauth2Service:
    return Oauth2Service(repository)

oauth2_service = Annotated[Oauth2Service, Depends(get_service)]


async def get_email_service(redis: RedisDep, repository: RepositoryDep) -> EmailService:
    return EmailService(redis, repository)

email_service = Annotated[EmailService, Depends(get_email_service)]


async def get_chat_service(repository: ChatRepositoryDep) -> ChatService:
    return ChatService(repository)

chat_service = Annotated[ChatService, Depends(get_chat_service)]
