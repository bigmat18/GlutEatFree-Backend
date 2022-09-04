import pytest
from utils.generate_random_string import generate_random_string
from models.Articles.Article import Article


def test_article_list(client, access_authorization):
    response = client.get('/articles', headers=access_authorization)
    assert response.status_code == 200
    assert isinstance(response.json(), list)



@pytest.mark.parametrize("title, status_code", [
    ("test", 201),
    (f"{generate_random_string(n=70)}", 422)
])
def test_article_create(client, access_authorization, title, status_code):
    data = {"title": title, "intro": "test"}
    response = client.post('/articles', data=data, headers=access_authorization)
    assert response.status_code == status_code



def test_article_retrieve(client, access_authorization, article):
    response = client.get(f'/article/{article.slug}', headers=access_authorization)
    assert response.status_code == 200



@pytest.mark.parametrize("title, status_code", [
    ("test", 200),
    (f"{generate_random_string(n=70)}", 422)
])
def test_article_update(client, access_authorization, article, title, status_code):
    data = {"title": title}
    response = client.patch(f'/article/{article.slug}', data=data, headers=access_authorization)
    assert response.status_code == status_code
    
def test_article_update_unauth(client, unauth_authorization, article):
    data = {"title": "test2"}
    response = client.patch(f'/article/{article.slug}', data=data, headers=unauth_authorization)
    
    assert response.status_code == 401



def test_article_delete(client, access_authorization, article):
    response = client.delete(f'/article/{article.slug}', headers=access_authorization)
    assert response.status_code == 204
    
def test_article_delete_unauth(client, unauth_authorization, article):
    response = client.delete(f'/article/{article.slug}', headers=unauth_authorization)
    assert response.status_code == 401