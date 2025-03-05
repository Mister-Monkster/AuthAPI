import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from DataBase.models import Base


load_dotenv()


engine = create_async_engine(
    url=os.getenv("DB_URL")
)


async_session = async_sessionmaker(engine, expire_on_commit=False)

