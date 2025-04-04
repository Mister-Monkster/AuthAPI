from Repositories.chat_repository import ChatRepository
from Schemas.ChatSchemas import ChatResponse
from utils.auth import decode_token


class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    @staticmethod
    async def is_authorize(access_token: str):
        if access_token:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            return user_id
        else:
            return False

    async def create_chat(self, access_token: str, to_user: int):
        try:
            if user_id := await self.is_authorize(access_token):
                data = {'user_1': user_id, 'user_2': to_user}
                res = await self.repository.create_chat_query(data)
                return res
            else:
                return None
        except Exception as e:
            print(e)
            return None

    async def get_chat(self, access_token: str, to_user: int):
        try:
            if user_id := await self.is_authorize(access_token):
                data = {'user_1': user_id, 'user_2': to_user}
                res = await self.repository.get_chat_query(data)
                return ChatResponse.model_validate(res)
            else:
                return None
        except Exception as e:
            print(e)
            return None

