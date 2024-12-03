import pytest
import httpx


host = "http://localhost:8000"


@pytest.mark.asyncio
async def test_create_user():
    # Login first
    login_response = httpx.post(
        f"{host}/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    try:
        assert login_response.status_code == 200
    except AssertionError:
        print(login_response.json())
        raise
    cookies = login_response.cookies

    response = httpx.post(
        f"{host}/api/v1/users",
        json={
            "username": "testuser1",
            "email": "user1@example.com",
            "password": "testpassworD123^",
            "full_name": "Test User",
        },
        cookies=cookies
    )
    data = response.json()

    try:
        assert response.status_code == 201
        assert data["email"] == "user1@example.com"
        assert data["username"] == "testuser1"
        assert data["full_name"] == "Test User"
        assert "id" in data
    except AssertionError:
        print(data)
        raise
    finally:
        if "id" in data:
            print(f"Deleting user {data['id']}")
            httpx.delete(f"{host}/api/v1/users/{data['id']}", cookies=cookies)


@pytest.mark.asyncio
async def test_create_duplicate_user():
    # Login first
    login_response = httpx.post(
        f"{host}/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    try:
        assert login_response.status_code == 200
    except AssertionError:
        print(login_response.json())
        raise
    cookies = login_response.cookies

    # Create first user
    httpx.post(
        f"{host}/api/v1/users",
        json={
            "username": "testuser2",
            "email": "user2@example.com",
            "password": "testpassworD123!",
            "full_name": "Test User",
        },
        cookies=cookies
    )

    # Try to create duplicate user
    response = httpx.post(
        f"{host}/api/v1/users",
        json={
            "username": "testuser2",
            "email": "user2@example.com",
            "password": "testpassworD123!",
            "full_name": "Test User",
        },
        cookies=cookies
    )
    try:
        assert response.status_code == 400
    except AssertionError:
        print(response.json())
        raise


@pytest.mark.asyncio
async def test_login_user():
    # Login as admin first
    admin_login = httpx.post(
        f"{host}/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    try:
        assert admin_login.status_code == 200
    except AssertionError:
        print(admin_login.json())
        raise
    cookies = admin_login.cookies

    # Create user first
    httpx.post(
        f"{host}/api/v1/users",
        json={
            "username": "testuser3",
            "email": "user3@example.com",
            "password": "testpassworD123#",
            "full_name": "Test User",
        },
        cookies=cookies
    )

    # Test login
    response = httpx.post(
        f"{host}/api/v1/auth/login",
        data={
            "username": "testuser3",
            "password": "testpassworD123#",
        },
    )
    data = response.json()
    try:
        assert response.status_code == 200
        assert "user_id" in data
    except AssertionError:
        print(data)
        raise


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    response = httpx.post(
        f"{host}/api/v1/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpassworD$",
        },
    )
    try:
        assert response.status_code == 401
    except AssertionError:
        print(response.json())
        raise


@pytest.mark.asyncio
async def test_get_current_user():
    # Login as admin first
    admin_login = httpx.post(
        f"{host}/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    try:
        assert admin_login.status_code == 200
    except AssertionError:
        print(admin_login.json())
        raise
    admin_cookies = admin_login.cookies

    # Create and login user
    create_response = httpx.post(
        f"{host}/api/v1/users",
        json={
            "username": "testuser4",
            "email": "user4@example.com",
            "password": "testpassworD123@",
            "full_name": "Test User",
        },
        cookies=admin_cookies
    )
    try:
        assert "id" in create_response.json()
    except AssertionError:
        print(create_response.json())
        raise

    user_id = create_response.json()["id"]

    # Login to get cookie
    login_response = httpx.post(
        f"{host}/api/v1/auth/login",
        data={"username": "testuser4", "password": "testpassworD123@"},
    )
    try:
        assert login_response.status_code == 200
    except AssertionError:
        print(login_response.json())
        httpx.delete(f"{host}/api/v1/users/{user_id}", cookies=admin_cookies)
        raise

    cookies = login_response.cookies

    # Get user by ID using cookie from login
    response = httpx.get(
        f"{host}/api/v1/users/{user_id}",  # Cookie set during login
        cookies=cookies
    )
    data = response.json()
    try:
        assert response.status_code == 200
        assert data["email"] == "user4@example.com"
        assert data["full_name"] == "Test User"
    except AssertionError:
        print(data)
        raise
    finally:
        httpx.delete(f"{host}/api/v1/users/{user_id}", cookies=admin_cookies)


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    response = httpx.get(
        f"{host}/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    try:
        assert response.status_code == 401
    except AssertionError:
        print(response.json())
        raise
