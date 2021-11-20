

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert len(response.json()) == 3
    assert response.status_code == 200