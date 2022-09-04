from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.Articles.Article import Article
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
    test = session.query(Article).filter(Article.title == "test").first()
    if test: return test
    article = Article(title="test", intro="test", author_id=user.id)
    session.add(article)
    session.commit()
    session.refresh(article)
    return article