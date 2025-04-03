import json
import random
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
import string
import secrets
from Schemas.UserSchemas import SPasswordChange
from utils.validators import email_validator
from Celery.tasks import send_mail, send_mail_recovery
from redis.asyncio import Redis
from Repositories.user_repository import UserRepository




class EmailService:
    def __init__(self, redis: Redis, repository: UserRepository):
        self.redis = redis
        self.repository = repository

    @staticmethod
    async def generate_code():
        return str(random.randint(100000, 999999))

    @staticmethod
    async def generate_token():
        token = secrets.token_urlsafe()
        return token

    async def mail_sender(self, to_email: str):
        subject = "Завершите регистрацию."
        code = await self.generate_code()
        send_mail.delay(code, to_email, subject)

    async def send_recovery_letter(self, to_email: str, subject: str):
        if email_validator(to_email):
            user = await self.repository.get_user_by_email(to_email)
            if user:
                token = await self.generate_token()
                send_mail_recovery.delay(token, to_email, subject)
                return True
            else:
                return False
        else:
            return False

    async def check_code(self, code: int, email: str, ):
        if cache := await self.redis.get(email):
            redis_code = json.loads(cache)
            if int(code) == int(redis_code):
                await self.repository.change_verification_status(email)
                await self.redis.delete(email)
                return True
            else:
                return False
        else:
            return False

    async def recovery(self, token: str, data: SPasswordChange):
        try:
            if email := await self.redis.get(str(token)):
                await self.repository.recovery_password_query(email, data.password)
                return True
            else:
                return None
        except Exception as e:
            raise e
