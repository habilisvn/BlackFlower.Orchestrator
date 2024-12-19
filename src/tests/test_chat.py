import httpx
import pytest
from os import getenv
from dotenv import load_dotenv


load_dotenv()
host = getenv("HOST")


@pytest.mark.asyncio
async def test_chat_endpoint():
    # Login first as admin
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

    # Prepare test data
    message = {"message": "Hello"}

    try:
        # Make request to chat endpoint
        response = httpx.post(
            f"{host}/api/v1/chat/completions", json=message, cookies=cookies
        )

        # Assert response
        assert response.status_code == 200
    except AssertionError:
        print(response.json())
        raise


@pytest.mark.asyncio
async def test_chat_endpoint_without_body():
    # Test with invalid data
    response = httpx.post(f"{host}/api/v1/chat/completions", json={})

    # Assert response
    assert response.status_code == 422  # Validation error
