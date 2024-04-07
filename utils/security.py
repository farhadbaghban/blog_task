from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends
from db.models.users import User
from db.engine import get_db

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user


def authenticate_user(username: str, password: str):
    user = get_user(username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
