import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers.user_router import auth_router
from routers.Oauth2_router import oauth2_router
from routers.recovery_router import recovery_router



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key='secret')


app.include_router(router=auth_router)
app.include_router(router=recovery_router)
app.include_router(router=oauth2_router)



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,

    )
