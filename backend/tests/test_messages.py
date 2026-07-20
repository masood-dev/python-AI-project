"""Test messages endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_get_messages_nonexistent_session():
    """Test getting messages for non-existent session returns 404."""
    response = client.get("/api/v1/sessions/invalid_id/messages")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_chat_nonexistent_session():
    """Test chat on non-existent session returns 404."""
    response = client.post(
        "/api/v1/sessions/invalid_id/messages",
        json={"content": "Hello"},
    )
    assert response.status_code == 404
