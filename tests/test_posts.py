from jose import jwt
from sqlalchemy.util.langhelpers import public_factory
from app import schemas
from app.config import settings


def test_get_all_posts(authorized_client, test_posts):
    """
    Test that we can get all posts.
    'test_posts' are sqlalchemy objects, not json objects.
    Validate response data using schema and turn into a list of dictionaries.
    """
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostVotes(**post)
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)

    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)
    assert posts_list[0].Post.id == test_posts[0].id


def test_unathorized_get_all_posts(client):
    """
    Test that we cannot get all posts without authorization.
    Use regular client, not authorized client.
    """
    response = client.get("/posts/")

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_post_by_id(authorized_client, test_posts):
    """
    Test that we can get a post by id.
    """
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVotes(**response.json())

    assert response.status_code == 200
    assert response.json()['Post']['id'] == test_posts[0].id
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_unathorized_get_post_by_id(client, test_posts):
    """
    Test that we cannot get a post by id without authorization.
    Use regular client, not authorized client.
    """
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_post_by_id_not_found(authorized_client, test_posts):
    """
    Test that we cannot get a post by id that does not exist.
    """
    response = authorized_client.get(f"/posts/{len(test_posts)+1}")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Post not found'}


def test_create_post(authorized_client):
    """
    Test that we can create a post.
    """
    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "published": True
    }
    response = authorized_client.post("/posts/", json=post_data)
    post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert response.json()['title'] == post_data['title']
    assert response.json()['content'] == post_data['content']
    assert post.title == post_data['title']
    assert post.content == post_data['content']
    assert post.owner_id is not None
    assert post.published is True


def test_unathorized_create_post(client):
    """
    Test that we cannot create a post without authorization.
    Use regular client, not authorized client.
    """
    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "published": True
    }
    response = client.post("/posts/", json=post_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_post_missing_title(authorized_client):
    """
    Test that we cannot create a post without a title.
    """
    post_data = {
        "content": "Test Content"
    }
    response = authorized_client.post("/posts/", json=post_data)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"


def test_create_post_missing_content(authorized_client):
    """
    Test that we cannot create a post without content.
    """
    post_data = {
        "title": "Test Post"
    }
    response = authorized_client.post("/posts/", json=post_data)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"


def test_create_post_missing_title_content(authorized_client):
    """
    Test that we cannot create a post without a title and content.
    """
    response = authorized_client.post("/posts/", json={})

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"


def test_update_post(authorized_client, test_posts):
    """
    Test that we can update a post.
    """
    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "published": False
    }
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}", json=post_data)
    post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert response.json()['title'] == post_data['title']
    assert response.json()['content'] == post_data['content']
    assert post.title == post_data['title']
    assert post.content == post_data['content']
    assert post.owner_id is not None
    assert post.published is False


def test_unathorized_update_post(client, test_posts):
    """
    Test that we cannot update a post without authorization.
    Use regular client, not authorized client.
    """
    post_data = {
        "title": "Test Post",
        "content": "Test Content"
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=post_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_post(authorized_client, test_posts):
    """
    Test that we can delete a post.
    """
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204


def test_unathorized_delete_post(client, test_posts):
    """
    Test that we cannot delete a post without authorization.
    Use regular client, not authorized client.
    """
    response = client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_post_not_found(authorized_client, test_posts):
    """
    Test that we cannot delete a post that does not exist.
    """
    response = authorized_client.delete(f"/posts/{len(test_posts)+1}")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Post not found'}


def test_vote_post(authorized_client, test_posts):
    """
    Test that we can vote on a post.
    """
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})  # upvote

    assert response.status_code == 201
    assert response.json()['message'] == "Succesfully added vote"


def test_unathorized_vote_post(client, test_posts):
    """
    Test that we cannot vote on a post without authorization.
    Use regular client, not authorized client.
    """
    response = client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})  # upvote

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
