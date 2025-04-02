import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


load_dotenv()


def get_db_url():
    return os.getenv('DB_URL')

def get_domain():
    return os.getenv('DOMAIN')


def get_auth_data():
    return {"secret_key": os.getenv("SECRET_KEY"), "algorithm":os.getenv("ALGORITHM")}


client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
redis_url = os.getenv("REDIS_URL")


engine = create_async_engine(
    url=get_db_url()
)


async_session = async_sessionmaker(engine, expire_on_commit=False)
