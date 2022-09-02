from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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
def refresh_authorization(tokens):
    return {'Authorization': f"Bearer {tokens['refresh_token']}"}