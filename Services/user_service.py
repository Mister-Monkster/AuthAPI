
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from Auth.auth import verify_password, create_access_token, create_refresh_token, decode_token
from DataBase.queries import get_user_query, create_user_query, get_user_by_id, update_user_data_query
from Schemas.UserSchemas import SRegistration, SLogin, SAuth


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

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)
        user_id = int(payload['sub'])
        user_data = await get_user_by_id(user_id, self.session)
        if payload is None:
            return {"status_code": 401, "detail": 'Невалидный токен'}
        access_token = create_access_token({"sub": f'{user_data.id}'})
        user_dict = SRegistration.model_validate(user_data).model_dump()
        user_dict.pop('password')
        return {"user": user_dict, "access_token": access_token}

    async def get_user_data(self, id: int):
        user_data = await get_user_by_id(id, self.session)
        user_dict = SRegistration.model_validate(user_data).model_dump()
        user_dict.pop('password')
        user = SAuth.model_validate(user_dict).model_dump()
        return user

    async def get_user_profile(self, access_token: str):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user_data = await get_user_by_id(user_id, self.session)
        return user_data

    async def update_user_data(self, access_token: str, new_data: SAuth):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            await update_user_data_query(user_id, new_data, self.session)
            return True
        except:
            return False
