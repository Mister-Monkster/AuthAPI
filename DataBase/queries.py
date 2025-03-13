
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from Auth.auth import get_password_hash
from DataBase.models import UserModel
from Schemas.UserSchemas import SLogin, SRegistration


async def get_user_query(user: SLogin, session: AsyncSession):
    query = select(UserModel).where(UserModel.email == user.email)
    res = await session.execute(query)
    user_data = res.scalars().one_or_none()
    return user_data


async def get_user_by_id(user_id: int, session: AsyncSession):
    query = select(UserModel).where(UserModel.id == user_id)
    res = await session.execute(query)
    user_data = res.scalars().one_or_none()
    return user_data


async def create_user_query(user: SRegistration, session: AsyncSession):
    user_dict = user.model_dump()
    user_dict['password'] = get_password_hash(user.password)
    new_user = UserModel(**user_dict)
    session.add(new_user)
    await session.commit()

