from sqlalchemy import select, desc, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased, selectinload

from DataBase.models import ChatModel, MessageModel, UserModel


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_message(self, text: str, user_id: int, chat_id: int):
        new_message = MessageModel(text=text, user_id=user_id, chat_id=chat_id)
        self.session.add(new_message)
        await self.session.commit()
        return new_message

    async def get_chat_query(self, data):
        user1_id, user2_id = data.values()
        query = (
            select(ChatModel)
            .where(
                (ChatModel.user_1 == user1_id) & (ChatModel.user_2 == user2_id) |
                (ChatModel.user_1 == user2_id) & (ChatModel.user_2 == user1_id)
            )
            .options(
                selectinload(ChatModel.messages_rel)
                .selectinload(MessageModel.user_rel)
                .load_only(UserModel.username)
            )
        )
        result = await self.session.execute(query)
        res = result.scalars().unique().one_or_none()
        return res

    async def create_chat_query(self, data, text: str):
        if chat := await self.get_chat_query(data):
            return chat
        new_chat = ChatModel(**data)
        self.session.add(new_chat)
        await self.session.commit()
        await self.send_message(text, data['user_1'], new_chat.id)
        return new_chat

    async def get_my_chats_query(self, user_id):
        last_msg_subq = (
            select(
                MessageModel.chat_id,
                func.max(MessageModel.sending_date).label("max_date")
            )
            .group_by(MessageModel.chat_id)
            .subquery()
        )
        query = (
            select(ChatModel)
            .where(
                (ChatModel.user_1 == user_id) | (ChatModel.user_2 == user_id)
            )
            .options(
                selectinload(
                    ChatModel.messages_rel.and_(
                        MessageModel.sending_date == last_msg_subq.c.max_date,
                        MessageModel.chat_id == ChatModel.id
                    )
                )
                .selectinload(MessageModel.user_rel)
                .load_only(UserModel.username)
            )
        )
        result = await self.session.execute(query)
        res = result.scalars().one()
        return res


    async def send_message_query(self, user_id: int, chat_id: int, text:str):
        new_message = MessageModel(user_id=user_id, chat_id=chat_id, text=text)
        self.session.add(new_message)
        await self.session.commit()
        return new_message
