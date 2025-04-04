from fastapi import APIRouter, HTTPException, Request

from Schemas.ChatSchemas import ChatResponse
from dependecies.service_depends import chat_service

chats_router = APIRouter(tags=['Чаты',], prefix='/chat')


@chats_router.post('/')
async def new_chat(request: Request, to_user: int, service: chat_service):
    access_token = request.cookies.get('users_access_token')
    res = await service.create_chat(access_token, to_user)
    if res:
        return {"ok": True, 'detail': res}
    else:
        raise HTTPException(status_code=401, detail='Not authorize')


@chats_router.get("/get-chat")
async def get_chat(request: Request, to_user: int, service: chat_service) -> ChatResponse:
    access_token = request.cookies.get('users_access_token')
    res = await service.get_chat(access_token, to_user)
    if res:
        return res
    else:
        raise HTTPException(status_code=401, detail='Not authorize')
