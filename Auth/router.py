from typing import Annotated

from fastapi import APIRouter, Depends, Query

from Auth.auth import get_password_hash
from Auth.dependencies import ServiceDep
from Schemas.UserSchemas import SRegistration

router = APIRouter()


@router.post('/registration')
async def register(user: SRegistration, service: ServiceDep):
    await service.registration(user)
    return {'ok': True}