from app import schemas
from .database import client, session

def test_create_user(client):
    response = client.post('/users/', json={
        "email": "abuelita@gmail.com",
        "password": "abc123"
    })
    new_user = schemas.User(**response.json())
    assert new_user.email == "abuelita@gmail.com"
    assert response.status_code == 201
