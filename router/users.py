from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from db.engine import get_db
from schemas.user_schema import UserAuth, UserUpdate, UserCreateLogin
from schemas.auth_schema import TokenData
from _exceptions import ValidationToken
from utils.jwt import JWTHandler
from operation.users import UserOpration

router = APIRouter()


@router.post("/", tags=["users"], summary="Create new user")
def create_user(user: UserCreateLogin = Body(), db: Session = Depends(get_db)):
    return UserOpration(db=db).create_user(user=user)


@router.get("/", response_model=List[UserAuth], tags=["users"])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        users = UserOpration(db=db).get_users(skip=skip, limit=limit)
        return users
    else:
        raise ValidationToken


@router.get("/{user_id}", tags=["users"])
def read_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    user = UserOpration(db=db).get_user(username=token_data.username)
    return user


@router.put("/", tags=["users"])
def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        user = UserOpration(db=db).update_user(
            new_user=user, old_user=token_data.username
        )
        return user
    else:
        raise ValidationToken


@router.delete("/", tags=["users"])
def delete_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    if token_data:
        user = UserOpration(db=db).delete_user(username=token_data.username)
    else:
        raise ValidationToken
    return user


@router.post("/login", tags=["users"])
def login(data: UserCreateLogin = Body(), db: Session = Depends(get_db)):
    token = UserOpration(db=db).login_user(data=data)
    return token
