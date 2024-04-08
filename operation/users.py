from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models.users import User
from utils.security import get_hashed_password, authenticate_user
from schemas.user_schema import UserCreateLogin, UserAuth
from _exceptions import UserAlreadyExists, UserNotFound
from utils.jwt import JWTHandler


class UserOpration:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user: UserCreateLogin):
        password = get_hashed_password(user.password)
        user.password = password
        user = User(**user.model_dump())
        with self.db as db:
            try:
                db.add(user)
                db.commit()
                return UserAuth(id=user.id, username=user.username)
            except IntegrityError:
                raise UserAlreadyExists

    def login_user(self, data: UserCreateLogin):
        user = authenticate_user(
            username=data.username, password=data.password, session=self.db
        )
        if user:
            username = user.username
            access_token = JWTHandler.generate_token(username=username)
            return access_token

        else:
            raise UserNotFound

    def get_user(self, username):
        with self.db as db:
            user = db.query(User).filter(User.username == username).first()
            if user is None:
                raise UserNotFound
            return UserAuth(id=user.id, username=user.username)

    def get_users(self, skip: int, limit: int):
        with self.db as db:
            return db.query(User).offset(skip).limit(limit).all()

    def update_user(self, new_user, old_user):
        with self.db as db:
            db_user = db.query(User).filter(User.username == old_user).first()
            if db_user is None:
                raise UserNotFound
            for var, value in vars(new_user).items():
                setattr(db_user, var, value)
            db.commit()
            db.refresh(db_user)
            return UserAuth(id=db_user.id, username=db_user.username)

    def delete_user(self, username):
        with self.db as db:
            db_user = db.query(User).filter(User.username == username).first()
            if db_user is None:
                raise UserNotFound
            db.delete(db_user)
            db.commit()
            return db_user
