from fastapi import APIRouter, HTTPException, Response, Request

from utils.dependencies import user_service, email_service
from Schemas.CommonScemas import MessageSchema
from Schemas.UserSchemas import SRegistration, SLogin, SAuth


auth_router = APIRouter(tags=['Аутентификация',])


@auth_router.post('/registration', summary='Регистрация🆕')
async def register(user: SRegistration, service: user_service, service2: email_service, response: Response) -> MessageSchema:
    to_email = user.email,
    subject = "Завершите регистрацию."
    await service2.mail_sender(to_email=to_email, subject=subject)
    data = await service.registration(user)
    refresh_token = data['refresh_token']
    access_token = data['access_token']
    response.set_cookie(key='users_refresh_token',
                        value=refresh_token,
                        httponly=True,
                        samesite='strict',
                        secure=True,
                        max_age=604800
                        )
    response.set_cookie(key="users_access_token", value=access_token,
                        httponly=True,
                        samesite='strict',
                        secure=True,
                        max_age=900)
    message = MessageSchema(ok=True, detail='Вы успешно прошли регистрацию. Проверьте указанный email')
    return message


@auth_router.post('/verification', summary='Подтверждение email')
async def email_verification(code: int,
                             request: Request,
                             service: user_service,
                             e_service: email_service):
    try:
        access_token = request.cookies.get('users_access_token')
        user = await service.get_user_profile(access_token)
        if not user.is_verificate:
            if await e_service.check_code(code, user.email):
                return {'ok': True, 'detail': 'Вы успешно прошли верификацию'}
            else:
                return {'ok': False, 'detail': "Введен неверный код"}

        else:
            return {'ok': True, "detail": "Вы уже верифицированы"}
    except:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')




@auth_router.post('/login', summary='Авторизация🆔')
async def login_user(service: user_service, response: Response, user: SLogin) -> dict:
    try:
        login = user.login
        password = user.password
        user_data = await service.login(user)
        refresh_token = user_data['refresh_token']
        access_token = user_data['access_token']
        response.set_cookie(key='users_refresh_token',
                            value=refresh_token,
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            max_age=604800
                            )
        response.set_cookie(key="users_access_token", value=access_token,
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            max_age=900)
        return {'ok': True, "detail": f"Вы успешно авторизовались, как пользователь: {user_data['user'].username}"
                                      f" Ваш access_token:{access_token}"}
    except:
        raise HTTPException(status_code=401, detail='Вы ввели неверные данные')


@auth_router.post('/refresh', summary="Обновление токена доступа ♻️")
async def refresh_token(
        request: Request,
        response: Response,
        service: user_service) -> SAuth:
    try:
        refresh_token = request.cookies.get('users_refresh_token')
        user_data = await service.refresh(refresh_token)
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


@auth_router.post('/logout', summary='Выход❌')
async def logout(response: Response) -> MessageSchema:
    response.delete_cookie(key='users_access_token')
    response.delete_cookie(key='users_refresh_token')
    message = MessageSchema.model_validate({'ok': True, 'detail': 'Вы успешно вышли из системы'})
    return message


@auth_router.get("/user/{id}",  summary='Получить данные пользователя')
async def get_user(id: int, service: user_service) -> SAuth:
    try:
        res = await service.get_user_data(id)
        return res
    except:
        raise HTTPException(status_code=404, detail="Не удалось найти пользователя по данному id")


@auth_router.get("/user/my-profile", summary='Получить мои данные')
async def get_user(request: Request, service: user_service):
    try:
        access_token = request.cookies.get('users_access_token')
        return await service.get_user_profile(access_token)
    except:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")


@auth_router.put('/user/update', summary='Изменение данных✏️')
async def update_user(requset: Request, response: Response, user_data: SAuth, service: user_service):
    access_token = requset.cookies.get('users_access_token')
    res = await service.update_user_data(access_token, user_data)
    if res:
        return {'ok': True, 'detail': "Данные успешно изменены"}
    else:
        return HTTPException(status_code=response.status_code, detail='Ошибка изменения данных')


