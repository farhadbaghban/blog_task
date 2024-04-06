from pydantic import BaseModel
from datetime import datetime


class CommentCreateUpdate(BaseModel):
    author_id: int
    content: str


class CommentSchema(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    post_id: int
