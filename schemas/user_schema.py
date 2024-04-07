from pydantic import BaseModel


class UserAuth(BaseModel):
    id: int
    username: str


class UserCreateLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str
