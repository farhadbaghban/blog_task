from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.engine import Base
from .tags import post_tag_association


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post")
    tags = relationship("Tag", secondary=post_tag_association, back_populates="posts")
