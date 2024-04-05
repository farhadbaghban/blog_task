from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from db.engine import get_db
from db.models.posts import Post
from db.models.comments import Comment

import schema

router = APIRouter()


@router.post("/", response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.model_dump(), created_at=datetime.now())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[schema.Post])
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


@router.get("/{post_id}", response_model=schema.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schema.Post)
def update_post(post_id: int, post: schema.PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for var, value in vars(post).items():
        setattr(db_post, var, value)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}", response_model=schema.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return db_post


@router.post("/{post_id}/comments", response_model=schema.Comment)
def create_comment(
    comment: schema.CommentCreateUpdate, post_id: int, db: Session = Depends(get_db)
):
    db_comment = Comment(
        **comment.model_dump(), created_at=datetime.now(), post_id=post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/{post_id}/comments", response_model=List[schema.Post])
def read_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return (
        db.query(Comment).offset(skip).limit(limit).filter(Comment.post_id == post_id)
    )


@router.delete("/{post_id}/comments/{comment_id}", response_model=schema.Comment)
def delete_comments(
    post_id: int,
    comment_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):

    db_comment = (
        db.query(Comment)
        .offset(skip)
        .limit(limit)
        .filter(Comment.post_id == post_id)
        .filter(Comment.id == comment_id)
        .first()
    )

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_comment)
    db.commit()
    return db_comment
