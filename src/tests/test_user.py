import pytest
from fastapi.testclient import TestClient

from src.common.base import Base
from src.common.dependencies import get_pg_engine
from src.main import app


@pytest.fixture(autouse=True)
async def setup():
    # Create async PostgreSQL database for testing
    engine = get_pg_engine("test_db")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    client = TestClient(app)

    # Clean up after test
    yield client


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_create_duplicate_user(client: TestClient):
    # Create first user
    client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )

    # Try to create duplicate user
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 400


def test_login_user(client: TestClient):
    # Create user first
    client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )

    # Test login
    response = client.post(
        "/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/token",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient):
    # Create and login user
    client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )

    login_response = client.post(
        "/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123",
        },
    )
    token = login_response.json()["access_token"]

    # Test get current user
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"


def test_get_current_user_invalid_token(client: TestClient):
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
