from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth import create_access_token, create_refresh_token
from DataBase.queries import create_oauth_user_query
from settings import client_id, client_secret


class Oauth2Service:
    def __init__(self,  session: AsyncSession):
        self.session = session
        self.oauth = OAuth()
        self.oauth.register(
            name='google',
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_id=client_id,
            client_secret=client_secret,
            client_kwargs={
                'scope': 'email openid profile',
                'redirect_uri': 'http://localhost:8000/auth'
            }
        )

    async def register_or_update(self, user_dict):
        id = await create_oauth_user_query(user_dict, self.session)
        access_token = create_access_token({'sub': id})
        refresh_token = create_refresh_token({'sub': id})
        return {"access_token": access_token, "refresh_token": refresh_token}