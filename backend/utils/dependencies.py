from typing import Annotated
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from Repositories.user_repository import UserRepository
from Services.user_service import UserService
from Services.oauth2_service import Oauth2Service
from settings import async_session
from Services.user_service import UserService
from Services.oauth2_service import Oauth2Service
from Services.email_service import EmailService


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

RepositoryDep = Annotated[UserRepository, Depends(get_repository)]


async def get_userservice(repository: RepositoryDep) -> UserService:
    return UserService(repository)

user_service = Annotated[UserService, Depends(get_userservice)]

async def get_service(repository: RepositoryDep) -> Oauth2Service:
    return Oauth2Service(repository)

oauth2_service = Annotated[Oauth2Service, Depends(get_service)]

async def get_redis():
    redis = Redis.from_url("redis://localhost:6379",
                         decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()

RedisDep = Annotated[Redis, Depends(get_redis)]


async def get_email_service(redis: RedisDep, repository: RepositoryDep) -> EmailService:
    return EmailService(redis, repository)

email_service = Annotated[EmailService, Depends(get_email_service)]




