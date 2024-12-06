from os import getenv
from dotenv import load_dotenv
import pytest
import httpx


load_dotenv()
host = getenv("HOST")


@pytest.mark.asyncio
async def test_create_node():
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

    # Create a test node
    response = httpx.post(
        f"{host}/api/v1/nodes",
        json={
            "label": "test-node-1",
            "name": "test_node1",
            "description": "Test node description",
            "ip_address": "192.168.1.100",
            "status": "active",
        },
        cookies=cookies,
    )
    data = response.json()

    try:
        assert response.status_code == 201
        assert data["message"] == "Node created successfully"
    except AssertionError:
        print(data)
        raise
    finally:
        httpx.delete(f"{host}/api/v1/nodes/test-node-1", cookies=cookies)


@pytest.mark.asyncio
async def test_create_duplicate_node():
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

    # Create first node
    httpx.post(
        f"{host}/api/v1/nodes",
        json={
            "label": "test-node-2",
            "name": "test_node2",
            "description": "Test node description",
            "ip_address": "192.168.1.101",
            "status": "active",
        },
        cookies=cookies,
    )

    try:
        # Try to create duplicate node
        response = httpx.post(
            f"{host}/api/v1/nodes",
            json={
                "label": "test-node-2",
                "name": "test_node2",
                "description": "Test node description",
                "ip_address": "192.168.1.101",
                "status": "active",
            },
            cookies=cookies,
        )
        assert response.status_code == 400
    except AssertionError:
        print(response.json())
        raise
    finally:
        httpx.delete(f"{host}/api/v1/nodes/test-node-2", cookies=cookies)


@pytest.mark.asyncio
async def test_get_node():
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

    # Create a test node
    response = httpx.post(
        f"{host}/api/v1/nodes",
        json={
            "label": "test-node-3",
            "name": "test_node3",
            "description": "Test node description",
            "ip_address": "192.168.1.102",
            "status": "active",
        },
        cookies=cookies,
    )
    try:
        assert response.status_code == 201
    except AssertionError:
        print(response.json())
        httpx.delete(f"{host}/api/v1/nodes/test-node-3", cookies=cookies)
        raise

    try:
        # Get node by label
        response = httpx.get(
            f"{host}/api/v1/nodes/test-node-3", cookies=cookies
        )
        data = response.json()
        assert response.status_code == 200
        assert data["label"] == "test-node-3"
        assert data["name"] == "test_node3"
        assert data["description"] == "Test node description"
        assert data["ip_address"] == "192.168.1.102"
        assert data["status"] == "active"
    except AssertionError:
        print(data)
        raise
    finally:
        httpx.delete(f"{host}/api/v1/nodes/test-node-3", cookies=cookies)


@pytest.mark.asyncio
async def test_get_nonexistent_node():
    # Login first as admin
    login_response = httpx.post(
        f"{host}/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    cookies = login_response.cookies

    response = httpx.get(
        f"{host}/api/v1/nodes/nonexistent-label", cookies=cookies
    )
    try:
        assert response.status_code == 404
    except AssertionError:
        print(response.json())
        raise
