import pytest
from app import models

@pytest.fixture
def test_vote(session, test_posts, test_user):
    """
    Create a vote for a post.
    """
    vote = models.Vote(
        post_id=test_posts[0].id,
        user_id=test_user['id']
    )
    session.add(vote)
    session.commit()


def test_vote_post(authorized_client, test_posts):
    """
    Test that we can vote on a post.
    """
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert response.status_code == 201
    assert response.json()['message'] == "Succesfully added vote"


def test_unathorized_vote_post(client, test_posts):
    """
    Test that we cannot vote on a post without authorization.
    Use regular client, not authorized client.
    """
    response = client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    """
    Test that we can vote on a post only once.
    """
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert response.status_code == 409
    assert response.json()['detail'] == "You have already voted for this post"


def test_vote_invalid_post(authorized_client, test_posts):
    """
    Test that we cannot vote on a post that does not exist.
    """
    response = authorized_client.post(
        "/vote/", json={"post_id": len(test_posts)+1, "dir": 1})

    assert response.status_code == 404
    assert response.json()['detail'] == "Post not found"


def test_vote_invalid_dir(authorized_client, test_posts):
    """
    Test that we cannot vote on a post with an invalid direction.
    """
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 3})

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value is less than or equal to 1"


def test_downvote_post(authorized_client,  test_posts, test_vote):
    """
    Test that we can downvote a post.
    """
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 0})

    assert response.status_code == 201
    assert response.json()['message'] == "Succesfully removed vote"
