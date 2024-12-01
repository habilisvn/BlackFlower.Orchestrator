import pytest
from fastapi.testclient import TestClient
import datetime

from src.common.base import Base
from src.common.dependencies import get_pg_sync_engine
from src.main import app
from sqlalchemy.orm import Session
from src.user.infra.orm import User


@pytest.fixture(autouse=True)
def setup():
    # Create async PostgreSQL database for testing
    engine = get_pg_sync_engine("test_db")
    Base.metadata.create_all(bind=engine)

    # Create all tables
    with Session(engine) as session:
        # Create admin user directly in database
        admin = User(
            username="admin",
            email="admin@example.com",
            password="admin",
            full_name="Admin User",
            created_at=datetime.datetime.now(datetime.UTC),
            updated_at=datetime.datetime.now(datetime.UTC),
        )

        session.add(admin)
        session.commit()

    client = TestClient(app)

    # Clean up after test
    yield client


def test_create_user(client: TestClient):
    # Login first
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    assert login_response.status_code == 200
    client.cookies = login_response.cookies

    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser1",
            "email": "user1@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert data["username"] == "testuser1"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_create_duplicate_user(client: TestClient):
    # Login first
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    assert login_response.status_code == 200
    client.cookies = login_response.cookies

    # Create first user
    client.post(
        "/api/v1/users/",
        json={
            "username": "testuser2",
            "email": "user2@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )

    # Try to create duplicate user
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser2",
            "email": "user2@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 400


def test_login_user(client: TestClient):
    # Login as admin first
    admin_login = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    assert admin_login.status_code == 200
    client.cookies = admin_login.cookies

    # Create user first
    client.post(
        "/api/v1/users/",
        json={
            "username": "testuser3",
            "email": "user3@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )

    # Test login
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "testuser3",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "wronguser",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient):
    # Login as admin first
    admin_login = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    assert admin_login.status_code == 200
    client.cookies = admin_login.cookies

    # Create and login user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser4",
            "email": "user4@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    user_id = create_response.json()["id"]

    # Login to get cookie
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser4", "password": "testpassword123"},
    )
    assert login_response.status_code == 200
    client.cookies = login_response.cookies

    # Get user by ID using cookie from login
    response = client.get(
        f"/api/v1/users/{user_id}",  # Use the httponly cookie set during login
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user4@example.com"
    assert data["full_name"] == "Test User"


def test_get_current_user_invalid_token(client: TestClient):
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
