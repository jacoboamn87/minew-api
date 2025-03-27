"""
Pytest configuration and fixtures for Minew API tests.
"""
import pytest
import responses
from minew_api.client import MinewAPIClient


@pytest.fixture
def mock_responses():
    """Fixture that enables and yields a responses mock."""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mock_client(mock_responses):
    """Fixture that returns a MinewAPIClient instance with mocked responses."""
    # Mock the login endpoint for authentication
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LOGIN_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {"token": "mock-token-123456"}
        },
        status=200
    )
    
    # Create client with mocked auth
    client = MinewAPIClient("test_user", "test_password")
    
    # Reset the mock responses after client authentication
    mock_responses.reset()
    
    return client