from fastapi import APIRouter, HTTPException, Request

from Schemas.ChatSchemas import ChatResponse
from dependecies.service_depends import chat_service

chats_router = APIRouter(tags=['Чаты',], prefix='/chat')


@chats_router.post('/')
async def new_chat(request: Request, to_user: int, message_text: str,  service: chat_service):
    access_token = request.cookies.get('users_access_token')
    res = await service.create_chat(access_token, to_user, message_text)
    if res:
        return {"ok": True, 'detail': res}
    else:
        raise HTTPException(status_code=401, detail='Server Error')


@chats_router.get("/get-chat")
async def get_chat(request: Request, to_user: int, service: chat_service) -> ChatResponse:
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.get_chat(access_token, to_user)
        if res:
            return res
        else:
            raise HTTPException(status_code=404, detail='Not found')
    except:
        raise HTTPException(status_code=500, detail="Server Error")


@chats_router.get("/my-chats")
async def get_my_chats(request: Request, service: chat_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.get_my_chats(access_token)
        if res:
            return res
        else:
           return {'ok': True, "detail": "Чатов нет"}
    except:
        raise HTTPException(status_code=500, detail="Server Error")


@chats_router.post("/{chat_id}/send_message")
async def send_message(request: Request, chat_id: int, text: str, service: chat_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.send_message(access_token, chat_id, text)
        if res:
            return {"ok": True, 'detail': 'Сообщение доставлено'}
        else:
            return {"ok": False, 'detail': 'Сообщение не доставлено'}
    except:
        raise HTTPException(status_code=500, detail="Server Error")


@chats_router.delete("/delete/{message_id}")
async def delete_message(request: Request, message_id: int, service: chat_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.delete_message(access_token, message_id)
        if res:
            return {"ok": True, 'detail': 'Сообщение удалено'}
        else:
            return {"ok": False, 'detail': 'Сообщение не удалено'}
    except:
        raise HTTPException(status_code=500, detail="Server Error")


@chats_router.delete('/delete-chat/{chat_id}')
async def delete_chat(request: Request, chat_id: int, service: chat_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.delete_message(access_token, chat_id)
        if res:
            return {"ok": True, 'detail': 'Чат удален'}
        else:
            return {"ok": False, 'detail': 'Чат не удален'}
    except:
        raise HTTPException(status_code=500, detail="Server Error")


