"""
Pytest configuration and fixtures for Minew API tests.
"""
import pytest
import responses
from minew_api.client import MinewAPIClient
from minew_api.base import BaseClient
from minew_api.resources.store import StoreResource
from minew_api.resources.gateway import GatewayResource
from minew_api.resources.label import LabelResource
from minew_api.resources.template import TemplateResource
from minew_api.resources.data import DataResource


@pytest.fixture
def mock_responses():
    """Fixture that enables and yields a responses mock."""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mock_base_client(mock_responses):
    """Fixture that returns a BaseClient instance with mocked authentication."""
    # Mock the login endpoint for authentication
    mock_responses.add(
        responses.POST,
        f"{BaseClient.BASE_URL}{BaseClient.LOGIN_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {"token": "mock-token-123456"}
        },
        status=200
    )
    
    # Create base client with mocked auth
    client = BaseClient("test_user", "test_password")
    
    # Reset the mock responses after client authentication
    mock_responses.reset()
    
    return client


@pytest.fixture
def mock_store_resource(mock_base_client):
    """Fixture that returns a StoreResource instance with mocked base client."""
    return StoreResource(mock_base_client)


@pytest.fixture
def mock_gateway_resource(mock_base_client):
    """Fixture that returns a GatewayResource instance with mocked base client."""
    return GatewayResource(mock_base_client)


@pytest.fixture
def mock_label_resource(mock_base_client):
    """Fixture that returns a LabelResource instance with mocked base client."""
    return LabelResource(mock_base_client)


@pytest.fixture
def mock_template_resource(mock_base_client):
    """Fixture that returns a TemplateResource instance with mocked base client."""
    return TemplateResource(mock_base_client)


@pytest.fixture
def mock_data_resource(mock_base_client):
    """Fixture that returns a DataResource instance with mocked base client."""
    return DataResource(mock_base_client)


@pytest.fixture
def mock_client(mock_responses):
    """Fixture that returns a MinewAPIClient instance with mocked responses."""
    # Mock the login endpoint for authentication
    mock_responses.add(
        responses.POST,
        f"{BaseClient.BASE_URL}{BaseClient.LOGIN_ENDPOINT}",
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