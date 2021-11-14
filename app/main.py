
from fastapi import FastAPI
import psycopg
from .database import engine
from . import models
from .routes import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg.connect()
    print("Connected!")
except:
    print("I am unable to connect to the database")

cur = conn.cursor(row_factory=psycopg.rows.dict_row)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
