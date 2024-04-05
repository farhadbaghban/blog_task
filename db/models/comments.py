from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.engine import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")
