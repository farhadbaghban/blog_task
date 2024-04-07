from pydantic import BaseModel
from datetime import datetime


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str
    content: str
