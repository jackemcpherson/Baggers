import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from baggers.database import Base, get_db
from baggers.main import app

# Use separate test database file for each test run
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_baggers.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create a test client with database dependency override"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Clean up test database file after all tests"""
    yield
    # Clean up the test database file
    if os.path.exists("test_baggers.db"):
        os.remove("test_baggers.db")
