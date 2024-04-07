from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.engine import get_db
from db.models.users import User
from schemas.user_schema import UserAuth, UserUpdate, UserCreate
from _exceptions import UserAlreadyExists
from utils.security import get_hashed_password


router = APIRouter()


@router.post("/", response_model=UserAuth, tags=["users"], summary="Create new user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print("start--------------")
    password = get_hashed_password(user.password)
    db_user = {"username": user.username, "password": password}
    with db:
        try:
            db.add(user)
            db.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_user)
        except IntegrityError:
            raise UserAlreadyExists


@router.get("/", response_model=List[UserAuth], tags=["users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserAuth, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserAuth, tags=["users"])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=UserAuth, tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
