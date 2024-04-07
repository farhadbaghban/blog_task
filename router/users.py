from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.engine import get_db
from db.models.users import User
from schemas.user_schema import UserAuth, UserUpdate, UserCreateLogin
from schemas.auth_schema import TokenData
from _exceptions import UserAlreadyExists, UserNotFound, ValidationToken
from utils.security import get_hashed_password, authenticate_user
from utils.jwt import JWTHandler

router = APIRouter()


@router.post("/", response_model=UserAuth, tags=["users"], summary="Create new user")
def create_user(user: UserCreateLogin = Body(), db: Session = Depends(get_db)):
    password = get_hashed_password(user.password)
    user.password = password
    db_user = User(**user.model_dump())
    with db:
        try:
            db.add(db_user)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"id": db_user.id, "username": db_user.username},
            )
        except IntegrityError:
            raise UserAlreadyExists


@router.get("/", response_model=List[UserAuth], tags=["users"])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        return db.query(User).offset(skip).limit(limit).all()
    else:
        raise ValidationToken


@router.get("/{user_id}", response_model=UserAuth, tags=["users"])
def read_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/", response_model=UserAuth, tags=["users"])
def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    db_user = db.query(User).filter(User.username == token_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/", response_model=UserAuth, tags=["users"])
def delete_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    db_user = db.query(User).filter(User.username == token_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


@router.post("/login", tags=["users"])
def login(data: UserCreateLogin = Body(), db: Session = Depends(get_db)):
    user = authenticate_user(username=data.username, password=data.password, session=db)
    if user:
        username = user.username
        access_token = JWTHandler.generate_token(username=username)
        return access_token

    else:
        raise UserNotFound
