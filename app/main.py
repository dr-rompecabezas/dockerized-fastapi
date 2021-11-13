
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils
from .routes import post, user, auth
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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
