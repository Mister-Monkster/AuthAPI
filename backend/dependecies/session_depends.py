from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from settings import async_session


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


async def get_redis():
    redis = Redis.from_url("redis://localhost:6379",
                         decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()

RedisDep = Annotated[Redis, Depends(get_redis)]
