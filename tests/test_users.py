from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, engine
from sqlalchemy.exc import IntegrityError
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from app import schemas
from app.config import settings
from app.database import get_db, Base
from app.main import app

# Point to fastapi_test database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Create fastapi_test database tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_create_user():
    response = client.post('/users/', json={
        "email": "abuelita@gmail.com",
        "password": "abc123"
    })
    new_user = schemas.User(**response.json())
    assert new_user.email == "abuelita@gmail.com"
    assert response.status_code == 201
