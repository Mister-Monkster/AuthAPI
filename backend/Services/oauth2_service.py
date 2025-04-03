from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth import create_access_token, create_refresh_token

from settings import client_id, client_secret
from Repositories.user_repository import UserRepository


class Oauth2Service:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.oauth = OAuth()
        self.oauth.register(
            name='google',
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_id=client_id,
            client_secret=client_secret,
            client_kwargs={
                'scope': 'email openid profile',
                'redirect_uri': 'http://localhost:5173/'
            }
        )

    async def register_or_update(self, user_dict):
        id = await self.repository.create_oauth_user_query(user_dict)
        access_token = create_access_token({'sub': f'{id}'})
        refresh_token = create_refresh_token({'sub': f'{id}'})
        return {"access_token": access_token, "refresh_token": refresh_token}