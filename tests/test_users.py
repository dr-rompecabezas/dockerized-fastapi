from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
import pytest
from app import schemas
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post('/users/', json={
        "email": "abuelita@gmail.com",
        "password": "abc123"
    })
    new_user = schemas.User(**response.json())
    assert new_user.email == "abuelita@gmail.com"
    assert response.status_code == 201
