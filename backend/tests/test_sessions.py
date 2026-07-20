"""Test sessions endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_create_session():
    """Test creating a new session."""
    response = client.post(
        "/api/v1/sessions",
        json={"title": "Test Session"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Session"
    assert "id" in data or "_id" in data


@pytest.mark.asyncio
async def test_list_sessions():
    """Test listing sessions."""
    response = client.get("/api/v1/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_nonexistent_session():
    """Test getting non-existent session returns 404."""
    response = client.get("/api/v1/sessions/invalid_id")
    assert response.status_code == 404
