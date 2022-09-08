import pytest

def test_comment_list(client, access_authorization, article):
    response = client.get(f"/article/{article.slug}/comments",
                          headers=access_authorization)
    assert response.status_code == 200

def test_comment_create(client, access_authorization, article):
    response = client.post(f"/article/{article.slug}/comments",
                           json={"content": "test"},
                           headers=access_authorization)
    assert response.status_code == 201

def test_comment_update(client, access_authorization, comment):
    response = client.patch(f"/article/comment/{comment.id}",
                           json={"content": "new test"},
                           headers=access_authorization)
    assert response.status_code == 200

def test_comment_delete(client, access_authorization, comment):
    response = client.delete(f"/article/comment/{comment.id}",
                           headers=access_authorization)
    assert response.status_code == 204