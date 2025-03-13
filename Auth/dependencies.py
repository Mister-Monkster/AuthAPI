from typing import Annotated

from fastapi import Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from Auth.auth import decode_token
from DataBase.models import UserModel
from Services.user_service import UserService
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


async def get_userservice(session: SessionDep) -> UserService:
    return UserService(session)


async def get_user(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        return None
    payload = decode_token(token)
    if payload:
        user_id = payload.get('sub')
        return int(user_id)
    else:
        print(payload)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Невалидный токен')

UserIdDep = Annotated[int, Depends(get_user)]

ServiceDep = Annotated[UserService, Depends(get_userservice)]
