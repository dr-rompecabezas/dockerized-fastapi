from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import psycopg
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    records = db.query(models.Post).all()
    return records


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    record = models.Post(**post.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    record = db.query(models.Post).filter(models.Post.id == id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return record


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    record = db.query(models.Post).filter(models.Post.id == id)

    if record.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    record.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    record_query = db.query(models.Post).filter(models.Post.id == id)
    record = record_query.first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    record_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return record_query.first()
