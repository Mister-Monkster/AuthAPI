from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Auth.auth import get_password_hash
from DataBase.models import UserModel
from Schemas.UserSchemas import SRegistration


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_service(self):
        return

    async def registration(self, user: SRegistration):
        user_dict = user.dict()
        user_dict['password'] = get_password_hash(user.password)
        new_user = UserModel(**user_dict)
        self.session.add(new_user)
        await self.session.commit()

    async def login(self):
        pass
