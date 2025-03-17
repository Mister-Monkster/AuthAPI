from fastapi import FastAPI
from routers.user_router import auth_router
from routers.Oauth2_router import oauth2_router


app = FastAPI()


app.include_router(router=auth_router)
app.include_router(router=oauth2_router)
