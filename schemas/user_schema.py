from uuid import UUID
from pydantic import BaseModel


class UserAuth(BaseModel):
    id: UUID
    username: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str
