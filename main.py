from contextlib import asynccontextmanager

from fastapi import FastAPI
from Auth.router import router


app = FastAPI()

app.include_router(router=router)