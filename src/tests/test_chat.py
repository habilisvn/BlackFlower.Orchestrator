from httpx import AsyncClient

from user.repr.api.chat import ChatMessage


async def test_chat_endpoint(client: AsyncClient):
    # Prepare test data
    message = ChatMessage(message="Hello")

    # Make request to chat endpoint
    response = await client.post("/chat", json=message.model_dump())

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"reply": "Received message!"}


async def test_chat_endpoint_invalid_data(client: AsyncClient):
    # Test with invalid data
    response = await client.post("/chat", json={})

    # Assert response
    assert response.status_code == 422  # Validation error
