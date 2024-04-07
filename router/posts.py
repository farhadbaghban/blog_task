from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body

from sqlalchemy.orm import Session
from db.engine import get_db
from db.models.posts import Post
from db.models.comments import Comment
from schemas.post_schema import PostCreate, PostSchema, PostUpdate
from schemas.comment_schema import CommentCreateUpdate, CommentSchema
from schemas.auth_schema import TokenData
from utils.jwt import JWTHandler
from utils.security import get_user
from _exceptions import IsNotYours, PostNotFound, CommentNotFound

router = APIRouter()


@router.post("/", response_model=PostSchema, tags=["posts"])
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    user = get_user(username=token_data.username, db=db)
    db_post = Post(**post.model_dump(), created_at=datetime.now(), author_id=user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[PostSchema], tags=["posts"])
def read_posts(
    author_id: int | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(Post)
    if author_id:
        query = query.filter(Post.author_id == author_id)
    if start_date:
        query = query.filter(Post.created_at >= start_date)
    if end_date:
        query = query.filter(end_date >= Post.created_at)
    return query.offset(skip).limit(limit).all()


@router.get("/{post_id}", response_model=PostSchema, tags=["posts"])
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostSchema, tags=["posts"])
def update_post(
    post_id: int,
    post: PostUpdate = Body(),
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise PostNotFound
    user = get_user(username=token_data.username, db=db)
    if user.id == db_post.author_id:
        for var, value in vars(post).items():
            setattr(db_post, var, value)
        db.commit()
        db.refresh(db_post)
        return db_post
    else:
        raise IsNotYours


@router.delete("/{post_id}", response_model=PostSchema, tags=["posts"])
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise PostNotFound
    user = get_user(username=token_data.username, db=db)
    if user.id == db_post.author_id:
        db.delete(db_post)
        db.commit()
        return db_post
    else:
        raise IsNotYours


@router.post("/{post_id}/comments", response_model=CommentSchema, tags=["comments"])
def create_comment(
    comment: CommentCreateUpdate,
    post_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):
    user = get_user(username=token_data.username, db=db)
    db_comment = Comment(
        **comment.model_dump(),
        created_at=datetime.now(),
        post_id=post_id,
        author_id=user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/{post_id}/comments", response_model=List[PostSchema], tags=["comments"])
def read_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return (
        db.query(Comment).offset(skip).limit(limit).filter(Comment.post_id == post_id)
    )


@router.delete(
    "/{post_id}/comments/{comment_id}", response_model=CommentSchema, tags=["comments"]
)
def delete_comments(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTHandler.verify_token),
):

    db_comment = (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .filter(Comment.id == comment_id)
        .first()
    )

    if db_comment is None:
        raise CommentNotFound
    user = get_user(username=token_data.username, db=db)
    if user.id == db_comment.author_id:
        db.delete(db_comment)
        db.commit()
        return db_comment
    else:
        raise IsNotYours
