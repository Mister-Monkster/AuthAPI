import json
import random
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Celery.tasks import send_mail
from DataBase.queries import change_verification_status


class EmailService:
    def __init__(self, redis: Redis, session: AsyncSession):
        self.redis = redis
        self.session = session

    @staticmethod
    async def generate_code():
        return str(random.randint(100000, 999999))

    async def mail_sender(self, to_email: str, subject: str):
        code = await self.generate_code()
        send_mail.delay(code, to_email, subject)

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



