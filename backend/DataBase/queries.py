from celery.worker.state import total_count
from sqlalchemy import update, select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth import get_password_hash
from utils.validators import email_validator
from DataBase.models import UserModel
from Schemas.UserSchemas import SLogin, SRegistration, SAuth, SPasswordChange, SProfile


async def get_user_query(user: SLogin, session: AsyncSession):
    if email_validator(user.login):
        query = select(UserModel).where(UserModel.email == user.login)
    else:
        query = select(UserModel).where(UserModel.username == user.login)
    res = await session.execute(query)
    user_data = res.scalars().one_or_none()
    return user_data


async def get_user_by_id(user_id: int, session: AsyncSession):
    query = select(UserModel).where(UserModel.id == user_id)
    res = await session.execute(query)
    user_data = res.scalars().one_or_none()
    return user_data


async def get_user_by_email(email:str, session: AsyncSession):
    query = select(UserModel).where(UserModel.email == email)
    res = await session.execute(query)
    user_data = res.scalars().one_or_none()
    return user_data


async def get_all_users_query(offset: int, session: AsyncSession, limit = 10, user_id: None|int = None) -> dict:
    if user_id:
        query = (select(
            UserModel.username,
            UserModel.bio,
            UserModel.is_verificate
        ).offset(offset).limit(limit).where(UserModel.id!=user_id))
    else:
        query = (select(
            UserModel.username,
            UserModel.bio,
            UserModel.is_verificate
        ).offset(offset).limit(limit))
    res = await session.execute(query)
    result = [SProfile.model_validate(item) for item in res.all()]
    return {
        "users": result,
        "total": len(result),
        "offset": offset,
        "limit": limit
    }


async def create_user_query(user: SRegistration, session: AsyncSession):
    user_dict = user.model_dump()
    user_dict['password'] = get_password_hash(user.password)
    new_user = UserModel(**user_dict)
    session.add(new_user)
    await session.commit()
    return new_user.id


async def update_user_data_query(user_id: int, new_data: SAuth, session: AsyncSession):
    values = new_data.model_dump()
    query = update(UserModel).where(UserModel.id == user_id).values(values)
    await session.execute(query)
    await session.commit()


async def update_user_password_query(user_id: int, password: str, session: AsyncSession):
    query = update(UserModel).where(UserModel.id == user_id).values({'password':get_password_hash(password)})
    await session.execute(query)
    await session.commit()


async def create_oauth_user_query(user_dict, session: AsyncSession):
    email = user_dict['email']
    user = await get_user_by_email(email, session)
    if user:
        query = update(UserModel).where(UserModel.email == email).values({"google_sub": user_dict['google_sub']})
        await session.execute(query)
        return user.id
    else:
        user = UserModel(**user_dict)
        session.add(user)
    await session.commit()
    return user.id


async def change_verification_status(email: str, session: AsyncSession):
    query = update(UserModel).where(UserModel.email == email). values({'is_verificate': True})
    await session.execute(query)
    await session.commit()


async def delete_user_query(user_id: int, session: AsyncSession):
    query = delete(UserModel).where(UserModel.id == user_id)
    await session.execute(query)
    await session.commit()


async def recovery_password_query(email: str, new_password: str, session: AsyncSession):
    query = update(UserModel).where(UserModel.email == email).values({'password': get_password_hash(new_password)})
    await session.execute(query)
    await session.commit()