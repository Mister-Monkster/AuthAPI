from sqlalchemy import select, desc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from DataBase.models import ChatModel, MessageModel, UserModel


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat_query(self, data):
        new_chat = ChatModel(**data)
        self.session.add(new_chat)
        await self.session.commit()
        return new_chat.id

    async def get_chat_query(self, data):
        user1_id, user2_id = sorted(data.values())
        Message = aliased(MessageModel)
        User = aliased(UserModel)
        query = select(ChatModel).where(
            ChatModel.user_1 == user1_id and ChatModel.user_2 == user2_id
            or
            ChatModel.user_1 == user2_id and ChatModel.user_2 == user1_id
        ).options(
            joinedload(ChatModel.messages_rel.of_type(Message))
            .joinedload(Message.user_rel)
        ).order_by(desc(Message.sending_date))
        result = await self.session.execute(query)
        res = result.scalars().unique().one_or_none()
        return res
