from fastapi import APIRouter, Response
from starlette.requests import Request
from utils.dependencies import oauth2_service

oauth2_router = APIRouter(tags=['Google Oauth2'])


@oauth2_router.get('/google', summary='Вход с помощью Google')
async def google_auth(request: Request, service: oauth2_service):
    redirect_uri = 'http://127.0.0.1:8000/auth'
    token = await service.oauth.google.authorize_redirect(request, redirect_uri)
    return token


@oauth2_router.get('/auth', summary='Вход с помощью Google')
async def auth(request: Request, response: Response, service: oauth2_service):
    token = await service.oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        user_data = {'email': user['email'], 'username': user['name'], 'google_sub': user['sub'], 'is_verificate': True}
        user_reg = await service.register_or_update(user_data)
        response.set_cookie(key='users_access_token',
                            value=user_reg['access_token'],
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            max_age=900)
        response.set_cookie(key='users_refresh_token',
                            value=user_reg['refresh_token'],
                            httponly=True,
                            samesite='strict',
                            secure=True,
                            max_age=604800
                            )
        return {'ok': True, 'detail': f'Вы успешно вошли через Google как {user['name']}'}




