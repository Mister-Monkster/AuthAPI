from pydantic import BaseModel


class JWTRefresh(BaseModel):
    id: int