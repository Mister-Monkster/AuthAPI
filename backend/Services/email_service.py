import json
import random
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
import string
import secrets

from Celery.tasks import send_mail, send_mail_recovery
from DataBase.queries import change_verification_status, get_user_by_email, recovery_password_query

from Schemas.UserSchemas import SPasswordChange


class EmailService:
    def __init__(self, redis: Redis, session: AsyncSession):
        self.redis = redis
        self.session = session

    @staticmethod
    async def generate_code():
        return str(random.randint(100000, 999999))

    @staticmethod
    async def generate_token():
        token = secrets.token_urlsafe()
        return token

    async def mail_sender(self, to_email: str, subject: str):
        code = await self.generate_code()
        send_mail.delay(code, to_email, subject)

    async def send_recovery_letter(self, to_email: str, subject: str):
        user = await get_user_by_email(to_email, self.session)
        if user:
            token = await self.generate_token()
            send_mail_recovery.delay(token, to_email, subject)
            return True
        else:
            return None

    async def check_code(self, code: int, email: str, ):
        if cache := await self.redis.get(email):
            redis_code = json.loads(cache)
            if int(code) == int(redis_code):
                await change_verification_status(email, self.session)
                await self.redis.delete(email)
                return True
            else:
                return False
        else:
            return False

    async def recovery(self, token: str, data: SPasswordChange):
        try:
            if email := await self.redis.get(str(token)):
                await recovery_password_query(email, data.password, self.session)
                return True
            else:
                return None
        except Exception as e:
            raise e
