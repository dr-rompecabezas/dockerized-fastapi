from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post('/users/', json={
        "email": "test_user@gmail.com",
        "password": "abc123"
    })
    new_user = schemas.User(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test_user@gmail.com"


def test_login_user(client, test_user):
    response = client.post('/login', data={
        "username": test_user['email'],
        "password": test_user['password']
    })
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert response.status_code == 200
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
