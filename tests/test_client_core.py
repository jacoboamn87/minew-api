"""
Tests for core functionality of the Minew API client classes.
"""
import pytest
import responses
import hashlib
from minew_api.client import MinewAPIClient
from minew_api.base import BaseClient
from minew_api.exceptions import APIError


def test_base_client_initialization(mock_responses):
    """Test base client initialization and authentication."""
    username = "test_user"
    password = "test_password"
    
    # Mock the login endpoint
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
    
    # Create client
    client = BaseClient(username, password)
    
    # Verify the authentication request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body
    
    # Verify password was hashed with MD5
    password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()
    assert password_md5 in request_body.decode()
    assert username in request_body.decode()
    
    # Verify token was set
    assert client.token == "mock-token-123456"


def test_client_initialization(mock_responses):
    """Test client initialization and composition with base client."""
    username = "test_user"
    password = "test_password"
    
    # Mock the login endpoint
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
    
    # Create client
    client = MinewAPIClient(username, password)
    
    # Verify token was passed through from base client
    assert client.token == "mock-token-123456"
    
    # Verify resource classes were properly initialized
    assert client._base_client is not None
    assert client._store is not None
    assert client._gateway is not None
    assert client._label is not None
    assert client._template is not None
    assert client._data is not None


def test_client_authentication_failure(mock_responses):
    """Test client behavior when authentication fails."""
    # Reset mock_responses to override the fixture's mock
    mock_responses.reset()
    
    # Mock a failed login
    mock_responses.add(
        responses.POST,
        f"{BaseClient.BASE_URL}{BaseClient.LOGIN_ENDPOINT}",
        json={
            "code": 400,
            "msg": "Invalid credentials",
            "data": None
        },
        status=200  # API returns 200 even for failures, with error code in JSON
    )
    
    # Attempt to create client, should raise an exception
    with pytest.raises(APIError) as excinfo:
        MinewAPIClient("wrong_user", "wrong_password")
    
    assert "Login failed" in str(excinfo.value)
    assert "400" in str(excinfo.value)
    assert "Invalid credentials" in str(excinfo.value)


def test_get_headers(mock_base_client):
    """Test header generation for API requests."""
    # Test default headers
    headers = mock_base_client.get_headers()
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == f"Bearer {mock_base_client.token}"
    
    # Test with extra headers
    extra_headers = {"X-Custom-Header": "value"}
    headers = mock_base_client.get_headers(extra_headers=extra_headers)
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == f"Bearer {mock_base_client.token}"
    assert headers["X-Custom-Header"] == "value"


def test_build_url(mock_base_client):
    """Test URL building for endpoints."""
    # Test with relative endpoint
    endpoint = "/test/endpoint"
    url = mock_base_client.build_url(endpoint)
    assert url == f"{BaseClient.BASE_URL}{endpoint}"


def test_request_methods(mock_base_client, mock_responses):
    """Test HTTP request methods."""
    # Test GET request
    endpoint = "/test/get"
    mock_responses.add(
        responses.GET,
        f"{BaseClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": {"key": "value"}},
        status=200
    )
    
    response = mock_base_client.get(endpoint)
    assert len(mock_responses.calls) == 1
    assert mock_responses.calls[0].request.method == "GET"
    
    # Test POST request
    endpoint = "/test/post"
    data = {"test": "data"}
    mock_responses.add(
        responses.POST,
        f"{BaseClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": {"key": "value"}},
        status=200
    )
    
    response = mock_base_client.post(endpoint, data)
    assert len(mock_responses.calls) == 2
    assert mock_responses.calls[1].request.method == "POST"
    assert mock_base_client.token in mock_responses.calls[1].request.headers["Authorization"]
    
    # Test PUT request
    endpoint = "/test/put"
    data = {"test": "data"}
    mock_responses.add(
        responses.PUT,
        f"{BaseClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": {"key": "value"}},
        status=200
    )
    
    response = mock_base_client.put(endpoint, data)
    assert len(mock_responses.calls) == 3
    assert mock_responses.calls[2].request.method == "PUT"
    
    # Test DELETE request
    endpoint = "/test/delete"
    mock_responses.add(
        responses.DELETE,
        f"{BaseClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": None},
        status=200
    )
    
    response = mock_base_client.delete(endpoint)
    assert len(mock_responses.calls) == 4
    assert mock_responses.calls[3].request.method == "DELETE"


def test_validate_response(mock_base_client, mock_responses):
    """Test response validation logic."""
    # Mock a request with non-200 HTTP status
    endpoint = "/test/error"
    mock_responses.add(
        responses.GET,
        f"{BaseClient.BASE_URL}{endpoint}",
        json={"error": "Internal server error"},
        status=500
    )
    
    # Should raise APIError for HTTP error
    with pytest.raises(APIError) as excinfo:
        mock_base_client.get(endpoint)
    
    assert "500" in str(excinfo.value)


def test_parse_response(mock_base_client):
    """Test response parsing logic."""
    # Create a mock response with successful code
    class MockResponse:
        def json(self):
            return {
                "code": 200,
                "msg": "success",
                "data": {"key": "value"}
            }
    
    response, code, msg = mock_base_client.parse_response(
        MockResponse(), 
        "Error: {code} - Message: {msg}"
    )
    
    assert code == 200
    assert msg == "success"
    assert response["data"]["key"] == "value"
    
    # Test with error code
    class MockErrorResponse:
        def json(self):
            return {
                "code": 400,
                "msg": "Bad request",
                "data": None
            }
    
    with pytest.raises(APIError) as excinfo:
        mock_base_client.parse_response(
            MockErrorResponse(), 
            "API Error: {code} - Message: {msg}"
        )
    
    assert "API Error: 400 - Message: Bad request" in str(excinfo.value)


def test_client_method_delegation(mock_client, mock_responses):
    """Test that MinewAPIClient correctly delegates to resource classes."""
    # Get the correct endpoint from StoreResource
    from minew_api.resources.store import StoreResource

    # Mock the store info endpoint
    mock_responses.add(
        responses.GET,
        f"{BaseClient.BASE_URL}{StoreResource.STORE_LIST_ENDPOINT}?active=1",
        json={
            "code": 200,
            "msg": "success",
            "data": [{"id": "store1", "name": "Test Store"}]
        },
        status=200
    )
    
    # Call the method through the client
    stores = mock_client.store_get_information()
    
    # Verify the request was made
    assert len(mock_responses.calls) == 1
    
    # Verify result is passed correctly
    assert len(stores) == 1
    assert stores[0]["id"] == "store1"