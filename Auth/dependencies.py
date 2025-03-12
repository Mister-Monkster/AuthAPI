from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models import UserModel
from Schemas.UserSchemas import RefreshRequest
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

#
# async def get_token(email:str, session: SessionDep) -> RefreshRequest | None:
#     query = select(UserModel.refresh_token).where(UserModel.email == email)
#     res = await session.execute(query)
#     refresh_token = res.one_or_none()
#     if refresh_token:
#         result = RefreshRequest.model_validate({'refresh_token':refresh_token})
#         return result
#     else:
#         return None

ServiceDep = Annotated[UserService, Depends(get_userservice)]
