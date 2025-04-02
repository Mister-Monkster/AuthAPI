from fastapi import APIRouter, Body

from utils.dependencies import email_service
from utils.validators import email_validator
from Schemas.UserSchemas import SPasswordRecovery

from DataBase.queries import get_user_by_email

recovery_router = APIRouter(tags=['Востановление пароля',], prefix='/recovery')


@recovery_router.post("/", summary="Отправка письма для сброса✉️")
async def password_recovery(service: email_service, email: str = Body(..., embed=True)):
    if email_validator(email):
        res = await service.send_recovery_letter(to_email=email, subject='Запрос на восстановление пароля')
        if res:
            return {'ok': True, 'detail': "Мы отправили письмо с дальнейшими инструкциями на указанную почту"}
        else:
            return {'ok': False, 'detail': "Пользователя с таким email не существует"}
    else:
        return {'ok': False, 'detail': "Вы ввели невалидный email"}


@recovery_router.put("/{token}", summary='Cброс пароля🔓')
async def password_recovery_change(service: email_service,
                                   token: str,
                                   data: SPasswordRecovery = Body(..., embed=True)):
    res = await service.recovery(token, data)
    if res:
        return {"ok": True, 'detail': "Пароль успешно изменен."}
    else:
        return {'ok': False, 'detail': "Срок действия ссылки уже истек. Повторите попытку."}

