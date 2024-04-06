from pydantic import BaseModel
from typing import Optional


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    id: Optional[str] = None
