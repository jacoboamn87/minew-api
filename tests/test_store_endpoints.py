"""
Tests for store management endpoints of the MinewAPIClient.
"""
import pytest
import responses
from minew_api.client import MinewAPIClient
from minew_api.exceptions import APIError


def test_store_add(mock_client, mock_responses):
    """Test adding a new store."""
    # Mock the store add endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_ADD_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {"storeId": "12345678"}
        },
        status=200
    )
    
    # Call the method
    store_id = mock_client.store_add(
        number="store123",
        name="Test Store",
        address="123 Test St"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "store123" in request_body
    assert "Test Store" in request_body
    assert "123 Test St" in request_body
    
    # Verify the result
    assert store_id == "12345678"


def test_store_modify(mock_client, mock_responses):
    """Test modifying an existing store."""
    # Mock the store update endpoint
    mock_responses.add(
        responses.PUT,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_UPDATE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.store_modify(
        id="12345678",
        name="Updated Store",
        address="456 New St",
        active=1
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "12345678" in request_body
    assert "Updated Store" in request_body
    assert "456 New St" in request_body
    
    # Verify the result
    assert result == "success"


def test_store_close_or_open(mock_client, mock_responses):
    """Test closing or opening a store."""
    # Mock the store active endpoint
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_ACTIVE_ENDPOINT}?storeId=12345678&active=1",
        json={
            "code": 200,
            "msg": "Store opened successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method to open the store
    result = mock_client.store_close_or_open(id="12345678", active=1)
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "Store opened successfully"
    
    # Test with invalid active value
    with pytest.raises(ValueError):
        mock_client.store_close_or_open(id="12345678", active=2)


def test_store_get_information(mock_client, mock_responses):
    """Test getting store information."""
    # Mock the store list endpoint
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_LIST_ENDPOINT}?active=1",
        json={
            "code": 200,
            "msg": "success",
            "data": [
                {
                    "id": "12345678",
                    "name": "Test Store",
                    "number": "store123",
                    "address": "123 Test St",
                    "active": 1
                }
            ]
        },
        status=200
    )
    
    # Call the method
    stores = mock_client.store_get_information(active=1)
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert isinstance(stores, list)
    assert len(stores) == 1
    assert stores[0]["id"] == "12345678"
    assert stores[0]["name"] == "Test Store"
    
    # Test with condition
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_LIST_ENDPOINT}?active=1&condition=Test",
        json={
            "code": 200,
            "msg": "success",
            "data": [
                {
                    "id": "12345678",
                    "name": "Test Store",
                    "number": "store123",
                    "address": "123 Test St",
                    "active": 1
                }
            ]
        },
        status=200
    )
    
    stores = mock_client.store_get_information(active=1, condition="Test")
    assert len(mock_responses.calls) == 2


def test_store_get_warnings(mock_client, mock_responses):
    """Test getting store warnings."""
    # Mock the store warnings endpoint
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_WARNING_ENDPOINT}?storeId=12345678",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "warnings": [
                    {
                        "id": "warning123",
                        "type": "battery",
                        "level": "critical",
                        "timestamp": "2023-01-01"
                    }
                ]
            }
        },
        status=200
    )
    
    # Call the method
    warnings = mock_client.store_get_warnings(store_id="12345678")
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert "warnings" in warnings["data"]
    assert len(warnings["data"]["warnings"]) == 1
    assert warnings["data"]["warnings"][0]["type"] == "battery"


def test_store_get_logs(mock_client, mock_responses):
    """Test getting store operation logs."""
    # Mock the store logs endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.STORE_LOGS_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "currentPage": 1,
                "pageSize": 10,
                "totalNum": 15,
                "isMore": 1,
                "totalPage": 2,
                "startIndex": 0,
                "items": [
                    {
                        "operator": "admin",
                        "createTime": "2023-01-01 12:00:00",
                        "actionType": "1",
                        "result": "1"
                    }
                ]
            }
        },
        status=200
    )
    
    # Call the method
    logs = mock_client.store_get_logs(
        store_id="12345678",
        current_page=1,
        page_size=10,
        object_type="1"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "12345678" in request_body
    assert "currentPage" in request_body
    
    # Verify the result
    assert "items" in logs["data"]
    assert logs["data"]["currentPage"] == 1
    assert logs["data"]["totalPage"] == 2