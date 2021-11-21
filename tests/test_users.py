import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    """
    Test that we can create a user.
    """
    response = client.post('/users/', json={
        "email": "test_user@gmail.com",
        "password": "abc123"
    })
    new_user = schemas.User(**response.json())

    assert response.status_code == 201
    assert new_user.email == "test_user@gmail.com"


def test_login_user(client, test_user):
    """
    Test that we can login a user and get a valid token in the response.
    Decode the token and validate the claims.
    """
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


@pytest.mark.parametrize('email, password, status_code', [
    ('wrong_email@gmail.com', 'abc123', 401),
    ('test_user@gmail.com', 'wrong_password', 401),
    (None, 'wrong_password', 422),
    ('test_user@gmail.com', None, 422)

])
def test_login_user_invalid_password(client, email, password, status_code):
    """
    Test that we cannot login an invalid user.
    """
    response = client.post('/login', data={
        "username": email,
        "password": password
    })
    
    assert response.status_code == status_code
