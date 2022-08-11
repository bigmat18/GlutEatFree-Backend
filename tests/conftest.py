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
