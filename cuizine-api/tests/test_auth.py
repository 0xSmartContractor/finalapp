import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.api.deps import (
    verify_auth_token,
    get_current_user,
    verify_subscription_access,
    get_rate_limit
)

@pytest.fixture
def mock_clerk():
    with patch('app.api.deps.clerk') as mock:
        yield mock

@pytest.fixture
def test_app(mock_clerk):
    app = FastAPI()
    
    @app.get("/test/auth")
    async def test_auth(user = Depends(get_current_user)):
        return {"id": user.id}
    
    @app.get("/test/subscription")
    async def test_subscription(user = Depends(verify_subscription_access)):
        return {"remaining": user.metadata.recipes_remaining}
    
    return TestClient(app)

def test_verify_auth_token(mock_clerk, test_app):
    # Arrange
    mock_clerk.clients.verify.return_value = {
        "id": "test_id",
        "sessions": [{"user_id": "user_1"}]
    }
    
    # Act
    response = test_app.get(
        "/test/auth",
        headers={"Authorization": "Bearer test_token"}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": "test_id"}

def test_verify_subscription_access(mock_clerk, test_app):
    # Arrange
    mock_clerk.clients.verify.return_value = {
        "id": "test_id",
        "sessions": [{"user_id": "user_1"}]
    }
    mock_clerk.users.get.return_value = {
        "id": "user_1",
        "email_addresses": [{"email_address": "test@example.com"}],
        "public_metadata": {
            "subscription_tier": "premium",
            "recipes_remaining": 10
        }
    }
    
    # Act
    response = test_app.get(
        "/test/subscription",
        headers={"Authorization": "Bearer test_token"}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"remaining": 10}

def test_rate_limit_exceeded(mock_clerk, test_app):
    # Arrange
    mock_clerk.clients.verify.return_value = {
        "id": "test_id",
        "sessions": [{"user_id": "user_1"}]
    }
    mock_clerk.users.get.return_value = {
        "id": "user_1",
        "public_metadata": {
            "subscription_tier": "free"
        }
    }
    
    # Act - Make requests until rate limit exceeded
    responses = [
        test_app.get(
            "/test/auth",
            headers={"Authorization": "Bearer test_token"}
        )
        for _ in range(12)  # Exceed free tier limit
    ]
    
    # Assert
    assert responses[-1].status_code == 429
    assert "Rate limit exceeded" in responses[-1].json()["error"]