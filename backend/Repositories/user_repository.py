from sqlalchemy.dialects.postgresql import insert
from celery.worker.state import total_count
from sqlalchemy import update, select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth import get_password_hash
from utils.validators import email_validator
from DataBase.models import UserModel
from Schemas.UserSchemas import SLogin, SRegistration, SAuth, SPasswordChange, SProfile


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_query(self, user: SLogin):
        if email_validator(user.login):
            query = select(UserModel).where(UserModel.email == user.login)
        else:
            query = select(UserModel).where(UserModel.username == user.login)
        res = await self.session.execute(query)
        user_data = res.scalars().one_or_none()
        return user_data

    async def get_user_by_id(self, user_id: int):
        query = select(UserModel).where(UserModel.id == user_id)
        res = await self.session.execute(query)
        user_data = res.scalars().one_or_none()
        return user_data

    async def get_user_by_email(self, email: str):
        query = select(UserModel).where(UserModel.email == email)
        res = await self.session.execute(query)
        user_data = res.scalars().one_or_none()
        return user_data

    async def get_all_users_query(self, offset: int, limit=10, user_id: None | int = None) -> dict:
        if user_id:
            query = (select(
                UserModel.username,
                UserModel.bio,
                UserModel.is_verificate
            ).offset(offset).limit(limit).where(UserModel.id != user_id))
        else:
            query = (select(
                UserModel.username,
                UserModel.bio,
                UserModel.is_verificate
            ).offset(offset).limit(limit))
        res = await self.session.execute(query)
        result = [SProfile.model_validate(item) for item in res.all()]
        return {
            "users": result,
            "total": len(result),
            "offset": offset,
            "limit": limit
        }

    async def create_user_query(self, user: SRegistration):
        user_dict = user.model_dump()
        user_dict['password'] = get_password_hash(user.password)
        new_user = UserModel(**user_dict)
        self.session.add(new_user)
        await self.session.commit()
        return new_user.id

    async def update_user_data_query(self, user_id: int, new_data: SAuth):
        values = new_data.model_dump()
        query = update(UserModel).where(UserModel.id == user_id).values(values)
        await self.session.execute(query)
        await self.session.commit()

    async def update_user_password_query(self, user_id: int, password: str):
        query = update(UserModel).where(UserModel.id == user_id).values({'password': get_password_hash(password)})
        await self.session.execute(query)
        await self.session.commit()

    async def create_oauth_user_query(self, user_dict):
        email = user_dict['email']
        user = await self.get_user_by_email(email)
        print(user)
        if user:
            query = update(UserModel).where(UserModel.email == email).values({"google_sub": user_dict['google_sub']})
            await self.session.execute(query)
        else:
            user = UserModel(**user_dict)
            self.session.add(user)
        await self.session.commit()
        return user.id

    async def change_verification_status(self, email: str):
        query = update(UserModel).where(UserModel.email == email).values({'is_verificate': True})
        await self.session.execute(query)
        await self.session.commit()

    async def delete_user_query(self, user_id: int):
        query = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(query)
        await self.session.commit()

    async def recovery_password_query(self, email: str, new_password: str):
        query = update(UserModel).where(UserModel.email == email).values({'password': get_password_hash(new_password)})
        await self.session.execute(query)
        await self.session.commit()