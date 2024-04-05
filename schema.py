from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int


class PostUpdate(BaseModel):
    title: str
    content: str


class CommentCreateUpdate(BaseModel):
    author_id: int
    content: str


class Comment(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    post_id: int
