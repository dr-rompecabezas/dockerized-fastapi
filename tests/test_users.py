from app import schemas
from .database import client, session

def test_create_user(client):
    response = client.post('/users/', json={
        "email": "test_user@gmail.com",
        "password": "abc123"
    })
    new_user = schemas.User(**response.json())
    assert new_user.email == "test_user@gmail.com"
    assert response.status_code == 201


def test_login_user(client):
    response = client.post('/login', data={
        "username": "test_user@gmail.com",
        "password": "abc123"
    })
    assert response.status_code == 200