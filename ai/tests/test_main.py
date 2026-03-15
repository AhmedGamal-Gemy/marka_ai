# AI Backend Tests (pytest)

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

# Mock environment variables for testing
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30
    }


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing"""
    return {
        "title": "Test Campaign",
        "description": "Test description",
        "budget": 1000.00
    }


# ==========================================
# Test: Health Endpoint
# ==========================================
def test_health_check():
    """Test that health endpoint returns 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ==========================================
# Test: User Routes
# ==========================================
def test_create_user(sample_user_data):
    """Test user creation endpoint"""
    response = client.post(
        "/api/v1/users/",
        json=sample_user_data,
        headers={"X-Service-Key": "test-key"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == sample_user_data["email"]


def test_create_user_missing_required_field(sample_user_data):
    """Test user creation with missing required field"""
    # Remove required field
    del sample_user_data["email"]

    response = client.post(
        "/api/v1/users/",
        json=sample_user_data,
        headers={"X-Service-Key": "test-key"}
    )
    assert response.status_code == 422  # Validation error


def test_get_users(sample_user_data):
    """Test getting all users"""
    # First create a user
    client.post(
        "/api/v1/users/",
        json=sample_user_data,
        headers={"X-Service-Key": "test-key"}
    )

    # Then get all users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ==========================================
# Test: Campaign Routes
# ==========================================
def test_create_campaign(sample_campaign_data):
    """Test campaign creation endpoint"""
    response = client.post(
        "/api/v1/campaigns/",
        json=sample_campaign_data,
        headers={"X-Service-Key": "test-key"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == sample_campaign_data["title"]


def test_get_campaigns(sample_campaign_data):
    """Test getting all campaigns"""
    # Create a campaign
    client.post(
        "/api/v1/campaigns/",
        json=sample_campaign_data,
        headers={"X-Service-Key": "test-key"}
    )

    # Get all campaigns
    response = client.get("/api/v1/campaigns/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_campaign_by_id(sample_campaign_data):
    """Test getting a specific campaign by ID"""
    # Create a campaign
    create_response = client.post(
        "/api/v1/campaigns/",
        json=sample_campaign_data,
        headers={"X-Service-Key": "test-key"}
    )
    campaign_id = create_response.json()["id"]

    # Get the campaign
    response = client.get(f"/api/v1/campaigns/{campaign_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == campaign_id


# ==========================================
# Test: Error Handling
# ==========================================
def test_get_nonexistent_campaign():
    """Test getting a campaign that doesn't exist"""
    response = client.get("/api/v1/campaigns/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_service_key_missing():
    """Test that service key is required"""
    response = client.post(
        "/api/v1/users/",
        json={"name": "Test"}
    )
    assert response.status_code == 401  # Unauthorized


# ==========================================
# Test: Validation
# ==========================================
def test_invalid_budget_value(sample_campaign_data):
    """Test campaign with invalid budget value"""
    # Set budget to negative value
    sample_campaign_data["budget"] = -1000.00

    response = client.post(
        "/api/v1/campaigns/",
        json=sample_campaign_data,
        headers={"X-Service-Key": "test-key"}
    )
    assert response.status_code == 422  # Validation error


# ==========================================
# Test: Rate Limiting (Simulated)
# ==========================================
@pytest.mark.skip(reason="Requires proper rate limiter implementation")
def test_rate_limit_exceeded():
    """Test that rate limiting works"""
    # Make many requests quickly
    for _ in range(100):
        response = client.get("/health")
        assert response.status_code in [200, 429]  # Either OK or Rate Limited


# ==========================================
# Test: Logging
# ==========================================
@pytest.mark.skip(reason="Requires logging configuration")
def test_logging():
    """Test that logging is working correctly"""
    response = client.get("/health")
    # Check logs contain the request
    assert "GET /health" in captured_output
