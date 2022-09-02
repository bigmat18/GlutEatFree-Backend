import pytest
from models.Articles.Article import Article
from models.User import User
from utils.generate_random_string import generate_random_string


@pytest.fixture()
def user(session):
    user = session.query(User).filter(User.email == "admin@admin.com").first()
    return user

@pytest.fixture()
def article(session, user):
    test = session.query(Article).filter(Article.title == "test").first()
    if test: return test
    article = Article(title="test", intro="test", author_id=user.id)
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


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
    print(title)
    response = client.post('/articles', data=data, headers=access_authorization)
    assert response.status_code == status_code
    
    
@pytest.mark.parametrize("title, status_code", [
    ("test", 200),
    (f"{generate_random_string(n=70)}", 422)
])
def test_article_update(client, access_authorization, article, title, status_code):
    data = {"title": title}
    print(title)
    response = client.patch(f'/article/{article.slug}', data=data, headers=access_authorization)
    assert response.status_code == status_code


def test_article_retrieve(client, access_authorization, article):
    response = client.get(f'/article/{article.slug}', headers=access_authorization)
    assert response.status_code == 200


def test_article_delete(client, access_authorization, article):
    response = client.delete(f'/article/{article.slug}', headers=access_authorization)
    assert response.status_code == 204