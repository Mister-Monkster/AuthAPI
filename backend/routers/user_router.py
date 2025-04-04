from fastapi import APIRouter, HTTPException, Response, Request, Body, Query


from Schemas.UserSchemas import SRegistration, SLogin, SAuth, SPasswordChange
from dependecies.service_depends import user_service, email_service

auth_router = APIRouter(tags=['Аутентификация',])


@auth_router.post('/registration', summary='Регистрация🆕')
async def register(user: SRegistration, service: user_service, service2: email_service, response: Response):
    try:
        to_email = user.email,
        await service2.mail_sender(to_email=to_email)
        data = await service.registration(user)
        refresh_token = data['refresh_token']
        access_token = data['access_token']
        response.set_cookie(key='users_refresh_token',
                            value=refresh_token,
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=604800
                            )
        response.set_cookie(key='users_access_token',
                            value=access_token,
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=900)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f'{e}')
    return {"ok": True, "detail" :"'Вы успешно прошли регистрацию. Проверьте указанный email"}


@auth_router.post('/verification', summary='Подтверждение email✅')
async def email_verification(
                             request: Request,
                             service: user_service,
                             e_service: email_service,
                             code: str = Body(..., embed=True)):
    try:
        access_token = request.cookies.get('users_access_token')
        user = await service.get_user_status(access_token)
        code = await e_service.check_code(int(code), user.email)
        if code and user:
            return {'ok':  True, 'detail': 'Вы успешно прошли верификацию'}
        else:
            return {'ok': True, "detail": "Вы уже верифицированы"}
    except:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')


@auth_router.post('/code-retry', summary='Повторная отправка кода🔁')
async def code_retry(request: Request, e_service:email_service, service: user_service):
    access_token = request.cookies.get('users_access_token')
    user = await service.get_user_profile(access_token)
    to_email = user.email,
    await e_service.mail_sender(to_email=to_email)
    return {"ok": True}


@auth_router.post('/login', summary='Авторизация🆔')
async def login_user(service: user_service, response: Response, user: SLogin) -> dict:
    try:
        user_data = await service.login(user)
        refresh_token = user_data['refresh_token']
        access_token = user_data['access_token']
        response.set_cookie(key='users_refresh_token',
                        value=refresh_token,
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=604800
                        )
        response.set_cookie(key='users_access_token',
                        value=access_token,
                        httponly=True,
                        samesite='lax',
                        secure=False,
                        max_age=900)
        return {'ok': True, "detail": f"Вы успешно авторизовались, как пользователь: {user_data['user'].username}"}
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
        response.set_cookie(key='users_access_token',
                            value=access_token,
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=900)
        return user_data['user']
    except:
        raise HTTPException(status_code=401, detail="Токен не найден или является невалидным.")


@auth_router.post('/logout', summary='Выход❌')
async def logout(response: Response):
    response.delete_cookie(key='users_access_token', httponly=True, samesite='lax', secure=False)
    response.delete_cookie(key='users_refresh_token', httponly=True, samesite='lax', secure=False)
    return {'ok': True, 'detail': 'Вы успешно вышли из системы'}


@auth_router.get("/user/{id}", summary="Получить данные пользователяℹ️")
async def get_user(id: int, service: user_service) -> SAuth:
    try:
        res = await service.get_user_data(id)
        return res
    except:
        raise HTTPException(status_code=404, detail="Не удалось найти пользователя по данному id")


@auth_router.get("/users", summary='Все пользователи')
async def get_all_users(request: Request, service: user_service, offset: int = Query(0, ge=0)):
    try:
        access_token = request.cookies.get('users_access_token')
        res = await service.get_users(offset, access_token=access_token)
        return res
    except:
        raise HTTPException(status_code=404, detail='Пользователи не найдены')


@auth_router.get("/my-profile", summary='Получить мои данныеℹ️')
async def get_user(request: Request, service: user_service):
    try:
        access_token = request.cookies.get('users_access_token')
        return await service.get_user_profile(access_token)

    except:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")


@auth_router.put('/user/update', summary='Изменение данных✏️')
async def update_user(request: Request, response: Response, user_data: SAuth, service: user_service):
    access_token = request.cookies.get('users_access_token')
    res = await service.update_user_data(access_token, user_data)
    if res:
        return {'ok': True, 'detail': "Данные успешно изменены"}
    else:
        return HTTPException(status_code=response.status_code, detail='Ошибка изменения данных')


@auth_router.put('/user/update-password', summary='Изменение пароля✏️')
async def update_user(request: Request, response: Response, password_schema: SPasswordChange, service: user_service):
    access_token = request.cookies.get('users_access_token')
    password = password_schema.new_password
    old_password = password_schema.old_password
    res = await service.update_user_password(access_token, password, old_password)
    response.delete_cookie(key='users_access_token', httponly=True, samesite='lax', secure=False)
    response.delete_cookie(key='users_refresh_token', httponly=True, samesite='lax', secure=False)
    if res:
        return {'ok': True, 'detail': "Пароль успешно изменен!"}
    else:
        return HTTPException(status_code=response.status_code, detail='Ошибка изменения данных')


@auth_router.delete("/user/delete", summary='Удалить профиль⛔️')
async def delete_profile(request: Request, response: Response, service: user_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.delete_user(access_token)
        response.delete_cookie(key='users_access_token', httponly=True, samesite='lax', secure=False)
        response.delete_cookie(key='users_refresh_token', httponly=True, samesite='lax', secure=False)
    except HTTPException:
        raise HTTPException(status_code=401, detail='Not authorize')


