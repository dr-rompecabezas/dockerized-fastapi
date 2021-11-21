from app import schemas

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
