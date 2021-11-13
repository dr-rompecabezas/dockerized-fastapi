from .database import engine, get_db
from . import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
from typing import List
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    conn = psycopg.connect()
    print("Connected!")
except:
    print("I am unable to connect to the database")

cur = conn.cursor(row_factory=psycopg.rows.dict_row)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("SELECT * FROM posts")
    # records = cur.fetchall()
    records = db.query(models.Post).all()
    return records


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # record = cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                      (post.title, post.content, post.published)).fetchone()
    # conn.commit()
    # record = models.Post(title=post.title, content=post.content, published=post.published)
    record = models.Post(**post.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # record = cur.execute("SELECT * FROM posts WHERE id = %s", (id,)).fetchone()
    record = db.query(models.Post).filter(models.Post.id == id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return record


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


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
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
    return record_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_to_update = user_query.first()
    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


@app.get("/users/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
