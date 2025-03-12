from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import Response
from fastapi.security import OAuth2PasswordBearer

from Auth.auth import get_password_hash, decode_token
from Auth.dependencies import ServiceDep
from Schemas.UserSchemas import SRegistration, SLogin, SAuth, RefreshRequest
from jose import JWTError

router = APIRouter()


@router.post('/registration')
async def register(user: SRegistration, service: ServiceDep):
    await service.registration(user)
    return {'ok': True}


@router.post('/login')
async def login_user(user: SLogin, service: ServiceDep, response: Response) -> SAuth:
    user_data = await service.login(user, response)
    return user_data


@router.post('/refresh')
async def refresh_token(
        request: RefreshRequest,
        response: Response,
        service: ServiceDep,
) -> SAuth:
    try:
        refresh_token = request.refresh_token
        payload = decode_token(refresh_token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        user_data = await service.refresh(email, refresh_token, response)
        return user_data
    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")
