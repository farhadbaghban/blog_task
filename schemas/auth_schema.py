from pydantic import BaseModel
from datetime import timedelta


class TokenData(BaseModel):
    username: str | None = None
    exp: timedelta | None = None


class TokenResponseSchema(BaseModel):
    access: str | None = None
