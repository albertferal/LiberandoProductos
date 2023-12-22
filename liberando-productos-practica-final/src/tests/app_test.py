"""
Module used for testing simple server module
"""

from fastapi.testclient import TestClient
import pytest

from application.app import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_read_health():
    """Tests the health check endpoint"""
    response = client.get("health")

    assert response.status_code == 200
    assert response.json() == {"health": "ok"}

@pytest.mark.asyncio
async def test_read_main():
    """Tests the main endpoint"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

@pytest.mark.asyncio
async def test_read_bye():
    """Tests the bye endpoint"""
    response = client.get("/bye")

    assert response.status_code == 200
    assert response.json() == {"msg": "Bye, have a nice day"}
