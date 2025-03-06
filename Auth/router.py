from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi import Response

from Auth.auth import get_password_hash
from Auth.dependencies import ServiceDep
from Schemas.UserSchemas import SRegistration, SLogin, SAuth

router = APIRouter()


@router.post('/registration')
async def register(user: SRegistration, service: ServiceDep):
    await service.registration(user)
    return {'ok': True}


@router.post('/login')
async def login_user(user: SLogin, service: ServiceDep, response: Response) -> SAuth:
    user_data = await service.login(user, response)
    return user_data
