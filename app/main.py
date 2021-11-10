from .database import engine, get_db
from . import models
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg.connect()
    print("Connected!")
except:
    print("I am unable to connect to the database")

cur = conn.cursor(row_factory=psycopg.rows.dict_row)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("SELECT * FROM posts")
    # records = cur.fetchall()
    records = db.query(models.Post).all()
    return {"data": records}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # record = cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                      (post.title, post.content, post.published)).fetchone()
    # conn.commit()
    # record = models.Post(title=post.title, content=post.content, published=post.published)
    record = models.Post(**post.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"data": record}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # record = cur.execute("SELECT * FROM posts WHERE id = %s", (id,)).fetchone()
    record = db.query(models.Post).filter(models.Post.id == id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": record}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # record = cur.execute(
    #     "DELETE FROM posts WHERE id = %s RETURNING *", (id,)).fetchone()
    record = db.query(models.Post).filter(models.Post.id == id)

    if record.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # conn.commit()
    record.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # record = cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                      (post.title, post.content, post.published, id)).fetchone()
    record_query = db.query(models.Post).filter(models.Post.id == id)
    record = record_query.first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # conn.commit()
    record_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": record_query.first()}
