
from fastapi import Depends, HTTPException, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from Auth.auth import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from DataBase.models import UserModel
from DataBase.queries import get_user_query, create_user_query, get_user_by_id
from Schemas.UserSchemas import SRegistration, SLogin, SAuth
from jose import JWTError


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def registration(self, user: SRegistration):
        await create_user_query(user, self.session)

    async def login(self, user: SLogin):
        user_data = await get_user_query(user, self.session)
        if user_data and verify_password(user.password, user_data.password):
            user_dict = SRegistration.model_validate(user_data).model_dump()
            user_dict.pop('password')
            access_token = create_access_token({"sub": f'{user_data.id}'})
            refresh_token = create_refresh_token({"sub": f'{user_data.id}'})
            return {"user": user_dict, "access_token": access_token, "refresh_token": refresh_token}

    async def refresh(self, user_id: int, refresh_token: str):
        user_data = await get_user_by_id(user_id, self.session)
        payload = decode_token(refresh_token)
        if payload is None:
            return {"status_code": 401, "detail": 'Невалидный токен'}
        access_token = create_access_token({"sub": f'{user_data.id}'})
        user_dict = SRegistration.model_validate(user_data).model_dump()
        user_dict.pop('password')
        return {"user": user_dict, "access_token": access_token}

    @staticmethod
    async def user_logout(response: Response, user_id: int):
        response.delete_cookie(key='users_access_token')
        response.delete_cookie(key='users_refresh_token')
        return {"ok": True, "detail": "Пользователь вышел из системы."}

    async def update_user_data(self):
        pass
