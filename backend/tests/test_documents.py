"""Test documents endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_list_documents_nonexistent_session():
    """Test listing documents for non-existent session returns 404."""
    response = client.get("/api/v1/sessions/invalid_id/documents")
    assert response.status_code == 404
