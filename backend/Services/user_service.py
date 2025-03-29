from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import verify_password, create_access_token, create_refresh_token, decode_token
from DataBase.queries import (get_user_query, create_user_query, get_user_by_id, update_user_data_query,
                              update_user_password_query, get_all_users_query)
from Schemas.UserSchemas import SRegistration, SLogin, SAuth, SPasswordChange



class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def registration(self, user: SRegistration):
        try:
            id = await create_user_query(user, self.session)
            access_token = create_access_token({"sub": f'{id}'})
            refresh_token = create_refresh_token({"sub": f'{id}'})
            return {"access_token": access_token, "refresh_token": refresh_token}
        except Exception:
            raise Exception

    async def login(self, user: SLogin):
        user_data = await get_user_query(user, self.session)
        if user_data and verify_password(user.password, user_data.password):
            access_token = create_access_token({"sub": f'{user_data.id}'})
            refresh_token = create_refresh_token({"sub": f'{user_data.id}'})
            return {"user": user_data, "access_token": access_token, "refresh_token": refresh_token}

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)
        user_id = int(payload['sub'])
        user_data = await get_user_by_id(user_id, self.session)
        if payload is None:
            return {"status_code": 401, "detail": 'Невалидный токен'}
        access_token = create_access_token({"sub": f'{user_data.id}'})
        user_dict = SAuth.model_validate(user_data).model_dump(exclude_unset=True)
        return {"user": user_dict, "access_token": access_token}

    async def get_user_data(self, id: int) -> SRegistration:
        user_data = await get_user_by_id(id, self.session)
        user_dict = SAuth.model_validate(user_data).model_dump(exclude_unset=True)
        return user_dict

    async def get_user_profile(self, access_token: str):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user_data = await get_user_by_id(user_id, self.session)
        return user_data

    async def get_users(self, offset: int, access_token: str):
        user_id = None
        if access_token:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
        users = await get_all_users_query(offset, self.session, user_id=user_id)
        return users

    async def update_user_data(self, access_token: str, new_data: SAuth):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            await update_user_data_query(user_id, new_data, self.session)
            return True
        except Exception:
            raise Exception

    async def update_user_password(self, access_token: str, password: str, old_password:str):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            user = await get_user_by_id(user_id, self.session)
            if verify_password(old_password, user.password):
                await update_user_password_query(user_id, password, self.session)
            else:
                return False
            return True
        except Exception:
            raise Exception



