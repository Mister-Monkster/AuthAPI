
from fastapi import Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Auth.auth import get_password_hash, verify_password, create_access_token
from DataBase.models import UserModel
from Schemas.UserSchemas import SRegistration, SLogin, SAuth


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_service(self):
        return

    async def registration(self, user: SRegistration):
        user_dict = user.model_dump()
        user_dict['password'] = get_password_hash(user.password)
        new_user = UserModel(**user_dict)
        self.session.add(new_user)
        await self.session.commit()

    async def login(self, user: SLogin, response) -> SAuth:
        query = (select(UserModel).where(
            UserModel.email == user.email))

        res = await self.session.execute(query)
        user_data = res.scalars().one_or_none()
        if user_data and verify_password(user.password, user_data.password):
            user_dict = SRegistration.model_validate(user_data).model_dump()
            user_dict.pop('password')
            access_token = create_access_token({"sub": user.email})
            response.set_cookie(key="users_access_token", value=access_token, httponly=True)
            return user_dict
        else:
            raise HTTPException(status_code=401, detail='Неправильный email или пароль.')

    async def logut(self):
        pass

    async def update_user_data(self):
        pass
