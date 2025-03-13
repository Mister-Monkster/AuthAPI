from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException, Response, Request

from Auth.auth import get_password_hash, decode_token
from Auth.dependencies import ServiceDep, get_user, UserIdDep
from Schemas.CommonScemas import MessageSchema
from Schemas.JWTSchemas import JWTRefresh
from Schemas.UserSchemas import SRegistration, SLogin, SAuth
from jose import JWTError

router = APIRouter()


@router.post('/registration', tags=['Аутентификация',], summary='Регистрация🆕')
async def register(user: SRegistration, service: ServiceDep) -> MessageSchema:
    await service.registration(user)
    response = MessageSchema.model_validate({'ok': True, 'detail': 'Вы успешно прошли регистрацию'})
    return response


@router.post('/login', tags=['Аутентификация',], summary='Авторизация🆔')
async def login_user(user: SLogin, service: ServiceDep, response: Response) -> SAuth:
    try:
        user_data = await service.login(user)
        refresh_token = user_data['refresh_token']
        access_token = user_data['access_token']
        response.set_cookie(key='users_refresh_token',
                            value=refresh_token,
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            )
        response.set_cookie(key="users_access_token", value=access_token,
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            max_age=900)
        return user_data['user']
    except:
        raise HTTPException(status_code=401, detail='Вы ввели неверные данные')


@router.post('/refresh', tags=['Аутентификация',], summary="Обновление токена доступа ♻️")
async def refresh_token(
        request: Request,
        response: Response,
        service: ServiceDep,
        user_id: UserIdDep
) -> SAuth:
    try:
        refresh_token = request.cookies.get('users_refresh_token')
        user_data = await service.refresh(user_id, refresh_token)
        access_token = user_data['access_token']
        response.set_cookie(key='users_refresh_token',
                            value=access_token,
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            max_age=900)
        return user_data['user']
    except:
        raise HTTPException(status_code=401, detail="Токен не найден или является невалидным.")


@router.post('/logout', tags=['Аутентификация',], summary='Выход❌')
async def logout(response: Response,
                 service: ServiceDep,
                 user_id: UserIdDep) -> MessageSchema:
    return await service.user_logout(response, user_id)
