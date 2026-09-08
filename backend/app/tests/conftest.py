"""
tests/conftest.py — Pytest fixtures shared across all test modules.

Test strategy:
  - We use SQLite in-memory as the test database (no MySQL required).
  - We override the `get_db` dependency to use the test session.
  - Each test function gets a fresh database with all tables created.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base, get_db
from app.main import app

# ── In-memory SQLite for tests ─────────────────────────────────────────────────
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite in FastAPI
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="function")
def db_session():
    """Fresh database session per test — tables created and dropped each time."""
    Base.metadata.create_all(bind=engine_test)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def client(db_session):
    """TestClient with the DB dependency overridden to use in-memory SQLite."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Helpers ────────────────────────────────────────────────────────────────────

def register_user(client, name="Test User", email="test@example.com", password="password123"):
    """Register a user and return the JSON response."""
    return client.post("/api/auth/register", json={
        "name": name, "email": email, "password": password
    })


def get_auth_headers(client, email="test@example.com", password="password123"):
    """Login and return Authorization header dict."""
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
