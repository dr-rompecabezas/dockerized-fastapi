from fastapi.testclient import TestClient
from sqlalchemy import create_engine, engine
from sqlalchemy.orm.session import sessionmaker
import pytest
from app.config import settings
from app.database import get_db, Base
from app.main import app
from app import models
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    """
    Create a session for interacting with the database.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    """
    Create a test client for interacting with the API.
    """
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    """
    Create a test user.
    """
    user_data = {
        "email": "test_user@gmail.com",
        "password": "abc123"
    }
    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    assert response.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    """
    Create a test client with an authorized token.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session):
    """
    Create multiple test posts.
    """
    posts_data = [{
        "title": "First Post",
        "content": "This is the first test post",
        "owner_id": test_user['id']
    }, {
        "title": "Second Post",
        "content": "This is the second test post",
        "owner_id": test_user['id']
    }, {
        "title": "Third Post",
        "content": "This is the third test post",
        "owner_id": test_user['id']
    }]

    def _create_post_model(post):
        return models.Post(**post)

    post_map = map(_create_post_model, posts_data)
    posts_list = list(post_map)

    session.add_all(posts_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
