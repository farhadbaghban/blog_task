from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from db.engine import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def __str__(self):
        return self.username
