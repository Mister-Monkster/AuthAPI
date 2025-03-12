import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from DataBase.models import Base


load_dotenv()


def get_db_url():
    return os.getenv('DB_URL')


def get_auth_data():
    return {"secret_key": os.getenv("SECRET_KEY"), "algorithm":os.getenv("ALGORITHM")}


engine = create_async_engine(
    url=get_db_url()
)


async_session = async_sessionmaker(engine, expire_on_commit=False)






# async def delete_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)