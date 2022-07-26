from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.Articles.Article import Article
from models.Articles.ArticleParagraph import ArticleParagraph, ArticleParagraphImage
from models.Articles.ArticleComment import ArticleComment
from models.User import User
import pytest


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/GEFLocalDB'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try: yield db
    finally: db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try: yield session
        finally: session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def tokens(client):
    response = client.post('/login', json={"email": "admin@admin.com", 
                                           "password":"admin123456"})
    return response.json()


@pytest.fixture()
def access_authorization(tokens):
    return {'Authorization': f"Bearer {tokens['access_token']}"}
    
    
@pytest.fixture()
def unauth_authorization(client, user_base):
    response = client.post('/login', json={"email": user_base.email,"password": user_base.password})
    return {'Authorization': f"Bearer {response.json()['access_token']}"}
    
    
@pytest.fixture()
def refresh_authorization(tokens):
    return {'Authorization': f"Bearer {tokens['refresh_token']}"}


@pytest.fixture()
def user(session):
    user = session.query(User).filter(User.email == "admin@admin.com").first()
    return user


@pytest.fixture()
def user_base(session):
    user = session.query(User).filter(User.email == "test@test.com").first()
    if not user:
        user = User(password="test", email="test@test.com")
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


@pytest.fixture()
def article(session, user):
    article = session.query(Article).filter(Article.title == "test").first()
    if not article:
        article = Article(title="test", intro="test", author_id=user.id)
        session.add(article)
        session.commit()
        session.refresh(article)
    return article


@pytest.fixture()
def paragraph(session, article):
    paragraph = session.query(ArticleParagraph).filter(ArticleParagraph.title == "test").first()
    if not paragraph:
        paragraph = ArticleParagraph(title="test", content="test", article_id=article.id)
        session.add(paragraph)
        session.commit()
        session.refresh(paragraph)
    return paragraph


@pytest.fixture()
def paragraph_image(session, paragraph):
    image = session.query(ArticleParagraphImage).filter(ArticleParagraphImage.caption == "test").first()
    if not image:
        image = ArticleParagraphImage(caption="test", image="url/test", paragraph_id=paragraph.id)
        session.add(image)
        session.commit()
        session.refresh(image)
    return image


@pytest.fixture()
def comment(session, article, user):
    comment = session.query(ArticleComment).filter(ArticleComment.content == "test").first()
    if not comment:
        comment = ArticleComment(content="test", article_id=article.id, author_id=user.id)
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment