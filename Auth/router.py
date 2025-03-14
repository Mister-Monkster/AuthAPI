from fastapi import APIRouter, HTTPException, Response, Request, Depends

from fastapi import APIRouter, HTTPException, Response, Request

from Auth.dependencies import ServiceDep
from Schemas.CommonScemas import MessageSchema
from Schemas.UserSchemas import SRegistration, SLogin, SAuth

router = APIRouter()


@router.post('/registration', tags=['Аутентификация',], summary='Регистрация🆕')
async def register(user: SRegistration, service: ServiceDep) -> MessageSchema:
    await service.registration(user)
    message = MessageSchema.model_validate({'ok': True, 'detail': 'Вы успешно прошли регистрацию'})
    return message


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
) -> SAuth:
    try:
        refresh_token = request.cookies.get('users_refresh_token')
        user_data = await service.refresh( refresh_token)
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
async def logout(response: Response) -> MessageSchema:
    response.delete_cookie(key='users_access_token')
    response.delete_cookie(key='users_refresh_token')
    message = MessageSchema.model_validate({'ok': True, 'detail': 'Вы успешно вышли из системы'})
    return message


@router.get("/user/{id}", tags=['Пользователи',], summary='Получить данные пользователя')
async def get_user(id: int, service: ServiceDep) -> SAuth:
    try:
        res = await service.get_user_data(id)
        return res
    except:
        raise HTTPException(status_code=404, detail="Не удалось найти пользователя по данному id")


@router.get("/my-profile", tags=['Пользователи',], summary='Получить мои данные')
async def get_user(request: Request, service: ServiceDep):
    try:
        access_token = request.cookies.get('users_access_token')
        return await service.get_user_profile(access_token)
    except:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")


@router.put('/user/update', tags=['Пользователи',], summary='Изменение данных✏️')
async def update_user(requset: Request, response: Response, user_data: SAuth, service:ServiceDep):
    access_token = requset.cookies.get('users_access_token')
    res = await service.update_user_data(access_token, user_data)
    if res:
        return {'ok': True, 'detail': "Данные успешно изменены"}
    else:
        return HTTPException(status_code=response.status_code, detail='Ошибка изменения данных')


