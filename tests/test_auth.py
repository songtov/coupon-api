import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import verify_password, get_password_hash, create_access_token
from app.models.user import UserRole
from datetime import datetime, timedelta

client = TestClient(app)

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    data = {"sub": "test@example.com", "role": "admin"}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    assert isinstance(token, str)
    assert len(token) > 0

@pytest.mark.asyncio
async def test_register_user_success(monkeypatch):
    mock_db = AsyncMock()
    mock_db.users.find_one.return_value = None
    mock_db.users.insert_one.return_value = AsyncMock(inserted_id="507f1f77bcf86cd799439011")
    mock_db.users.find_one.return_value = {
        "_id": "507f1f77bcf86cd799439011",
        "email": "test@example.com",
        "name": "Test User",
        "role": "client",
        "hashed_password": "hashedpassword"
    }
    
    async def mock_get_db():
        return mock_db
    
    from app.api.auth import get_db
    monkeypatch.setattr("app.api.auth.get_db", lambda: mock_get_db())
    
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "role": "client",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["role"] == "client"
    assert "password" not in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_register_user_email_exists(monkeypatch):
    mock_db = AsyncMock()
    mock_db.users.find_one.return_value = {"email": "existing@example.com"}
    
    async def mock_get_db():
        return mock_db
    
    monkeypatch.setattr("app.api.auth.get_db", lambda: mock_get_db())
    
    response = client.post(
        "/api/auth/register",
        json={
            "email": "existing@example.com",
            "name": "Test User",
            "role": "client",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]