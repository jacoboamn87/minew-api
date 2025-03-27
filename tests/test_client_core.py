"""
Tests for core functionality of the MinewAPIClient class.
"""
import pytest
import responses
import hashlib
from minew_api.client import MinewAPIClient
from minew_api.exceptions import APIError


def test_client_initialization(mock_responses):
    """Test client initialization and authentication."""
    username = "test_user"
    password = "test_password"
    
    # Mock the login endpoint
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
    
    # Create client
    client = MinewAPIClient(username, password)
    
    # Verify the authentication request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body
    
    # Verify password was hashed with MD5
    password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()
    assert password_md5 in request_body.decode()
    assert username in request_body.decode()
    
    # Verify token was set
    assert client.token == "mock-token-123456"


def test_client_authentication_failure(mock_responses):
    """Test client behavior when authentication fails."""
    # Reset mock_responses to override the fixture's mock
    mock_responses.reset()
    
    # Mock a failed login
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LOGIN_ENDPOINT}",
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


def test_get_headers(mock_client):
    """Test header generation for API requests."""
    # Test default headers
    headers = mock_client.get_headers()
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == f"Bearer {mock_client.token}"
    
    # Test with extra headers
    extra_headers = {"X-Custom-Header": "value"}
    headers = mock_client.get_headers(extra_headers=extra_headers)
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == f"Bearer {mock_client.token}"
    assert headers["X-Custom-Header"] == "value"


def test_build_url(mock_client):
    """Test URL building for endpoints."""
    # Test with relative endpoint
    endpoint = "/test/endpoint"
    url = mock_client.build_url(endpoint)
    assert url == f"{MinewAPIClient.BASE_URL}{endpoint}"


def test_request_methods(mock_client, mock_responses):
    """Test HTTP request methods."""
    # Test GET request
    endpoint = "/test/get"
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": {"key": "value"}},
        status=200
    )
    
    response = mock_client.get(endpoint)
    assert len(mock_responses.calls) == 1
    assert mock_responses.calls[0].request.method == "GET"
    
    # Test POST request
    endpoint = "/test/post"
    data = {"test": "data"}
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": {"key": "value"}},
        status=200
    )
    
    response = mock_client.post(endpoint, data)
    assert len(mock_responses.calls) == 2
    assert mock_responses.calls[1].request.method == "POST"
    assert mock_client.token in mock_responses.calls[1].request.headers["Authorization"]
    
    # Test PUT request
    endpoint = "/test/put"
    data = {"test": "data"}
    mock_responses.add(
        responses.PUT,
        f"{MinewAPIClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": {"key": "value"}},
        status=200
    )
    
    response = mock_client.put(endpoint, data)
    assert len(mock_responses.calls) == 3
    assert mock_responses.calls[2].request.method == "PUT"
    
    # Test DELETE request
    endpoint = "/test/delete"
    mock_responses.add(
        responses.DELETE,
        f"{MinewAPIClient.BASE_URL}{endpoint}",
        json={"code": 200, "msg": "success", "data": None},
        status=200
    )
    
    response = mock_client.delete(endpoint)
    assert len(mock_responses.calls) == 4
    assert mock_responses.calls[3].request.method == "DELETE"


def test_validate_response(mock_client, mock_responses):
    """Test response validation logic."""
    # Mock a request with non-200 HTTP status
    endpoint = "/test/error"
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{endpoint}",
        json={"error": "Internal server error"},
        status=500
    )
    
    # Should raise APIError for HTTP error
    with pytest.raises(APIError) as excinfo:
        mock_client.get(endpoint)
    
    assert "500" in str(excinfo.value)


def test_parse_response(mock_client):
    """Test response parsing logic."""
    # Create a mock response with successful code
    class MockResponse:
        def json(self):
            return {
                "code": 200,
                "msg": "success",
                "data": {"key": "value"}
            }
    
    response, code, msg = mock_client.parse_response(
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
        mock_client.parse_response(
            MockErrorResponse(), 
            "API Error: {code} - Message: {msg}"
        )
    
    assert "API Error: 400 - Message: Bad request" in str(excinfo.value)