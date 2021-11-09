from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg
from dotenv import load_dotenv
load_dotenv()

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
def get_posts():
    cur.execute("SELECT * FROM posts")
    records = cur.fetchall()
    return {"data": records}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    record = cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                         (post.title, post.content, post.published)).fetchone()
    conn.commit()
    return {"data": record}


@app.get("/posts/{id}")
def get_post(id: int):
    record = cur.execute("SELECT * FROM posts WHERE id = %s", (id,)).fetchone()
    if record is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": record}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    record = cur.execute(
        "DELETE FROM posts WHERE id = %s RETURNING *", (id,)).fetchone()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    record = cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                         (post.title, post.content, post.published, id)).fetchone()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    conn.commit()
    return {"data": record}
