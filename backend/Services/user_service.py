from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import verify_password, create_access_token, create_refresh_token, decode_token
from Schemas.UserSchemas import SRegistration, SLogin, SAuth, SPasswordChange

from Repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def registration(self, user: SRegistration):
        try:
            SRegistration.model_validate(user)
            id = await self.repository.create_user_query(user)
            access_token = create_access_token({"sub": f'{id}'})
            refresh_token = create_refresh_token({"sub": f'{id}'})
            return {"access_token": access_token, "refresh_token": refresh_token}
        except Exception:
            raise Exception

    async def login(self, user: SLogin):
        user_data = await self.repository.get_user_query(user)
        if user_data and verify_password(user.password, user_data.password):
            access_token = create_access_token({"sub": f'{user_data.id}'})
            refresh_token = create_refresh_token({"sub": f'{user_data.id}'})
            return {"user": user_data, "access_token": access_token, "refresh_token": refresh_token}

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)
        user_id = int(payload['sub'])
        user_data = await self.repository.get_user_by_id(user_id)
        if payload is None:
            return {"status_code": 401, "detail": 'Невалидный токен'}
        access_token = create_access_token({"sub": f'{user_data.id}'})
        user_dict = SAuth.model_validate(user_data).model_dump(exclude_unset=True)
        return {"user": user_dict, "access_token": access_token}

    async def get_user_data(self, id: int) -> SRegistration:
        user_data = await self.repository.get_user_by_id(id)
        user_dict = SAuth.model_validate(user_data).model_dump(exclude_unset=True)
        return user_dict

    async def get_user_status(self, access_token: str):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user_data = await self.repository.get_user_by_id(user_id)
        if not user_data.is_verificate:
            return True
        else:
            return False

    async def get_user_profile(self, access_token):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user_data = await self.repository.get_user_by_id(user_id)
        return user_data

    async def get_users(self, offset: int, access_token: str):
        user_id = None
        if access_token:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
        users = await self.repository.get_all_users_query(offset, user_id=user_id)
        return users

    async def update_user_data(self, access_token: str, new_data: SAuth):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            await self.repository.update_user_data_query(user_id, new_data)
            return True
        except Exception:
            raise Exception

    async def update_user_password(self, access_token: str, password: str, old_password:str):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            user = await self.repository.get_user_by_id(user_id)
            if verify_password(old_password, user.password):
                await self.repository.update_user_password_query(user_id, password)
            else:
                return False
            return True
        except Exception:
            raise Exception

    async def delete_user(self, access_token: str):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            await self.repository.delete_user_query(user_id)
            return True
        except Exception:
            raise Exception




