"""
Tests for gateway management endpoints of the MinewAPIClient.
"""
import pytest
import responses
from minew_api.client import MinewAPIClient
from minew_api.exceptions import APIError


def test_gateway_add(mock_client, mock_responses):
    """Test adding a new gateway."""
    # Mock the gateway add endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.GATEWAY_ADD_ENDPOINT}",
        json={
            "code": 200,
            "message": "success",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.gateway_add(
        mac="AC233FC03CEC",
        name="GW-AC233FC03CEC",
        store_id="1328266049345687552"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "AC233FC03CEC" in request_body
    assert "GW-AC233FC03CEC" in request_body
    assert "1328266049345687552" in request_body
    
    # Verify the result
    assert result == "success"


def test_gateway_delete(mock_client, mock_responses):
    """Test deleting a gateway."""
    # Mock the gateway delete endpoint
    gateway_id = "1349244935877955584"
    store_id = "1328266049345687552"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.GATEWAY_DELETE_ENDPOINT}?id={gateway_id}&storeId={store_id}",
        json={
            "code": 200,
            "message": "success",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.gateway_delete(
        gateway_id=gateway_id,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "success"


def test_gateway_list(mock_client, mock_responses):
    """Test listing gateways."""
    # Mock the gateway list endpoint
    store_id = "1326065100695539712"
    page = 1
    size = 10
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.GATEWAY_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}",
        json={
            "code": 200,
            "msg": "success",
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 2,
            "isMore": 0,
            "totalPage": 1,
            "startIndex": 0,
            "items": [
                {
                    "id": "gateway1",
                    "name": "Gateway 1",
                    "mac": "AC233FC03CEC",
                    "mode": 1,
                    "hardware": "v1.0",
                    "firmware": "v2.0",
                    "product": "GW-101",
                    "createTime": "2023-01-01",
                    "updateTime": "2023-01-02"
                },
                {
                    "id": "gateway2",
                    "name": "Gateway 2",
                    "mac": "AC233FC03CED",
                    "mode": 0,
                    "hardware": "v1.0",
                    "firmware": "v2.0",
                    "product": "GW-101",
                    "createTime": "2023-01-03",
                    "updateTime": "2023-01-04"
                }
            ]
        },
        status=200
    )
    
    # Call the method
    gateways = mock_client.gateway_list(
        store_id=store_id,
        page=page,
        size=size
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert len(gateways) == 2
    assert gateways[0]["id"] == "gateway1"
    assert gateways[1]["mac"] == "AC233FC03CED"


def test_gateway_modify(mock_client, mock_responses):
    """Test modifying a gateway."""
    # Mock the gateway update endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.GATEWAY_UPDATE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.gateway_modify(
        gateway_id="1339854807833251840",
        name="AC233FC03D511"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "1339854807833251840" in request_body
    assert "AC233FC03D511" in request_body
    
    # Verify the result
    assert result == "success"


def test_gateway_restart(mock_client, mock_responses):
    """Test restarting a gateway."""
    # Mock the gateway restart endpoint
    gateway_id = "gateway123"
    store_id = "store123"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.GATEWAY_RESTART_ENDPOINT}?id={gateway_id}&storeId={store_id}",
        json={
            "code": 200,
            "msg": "Gateway restart initiated",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.gateway_restart(
        gateway_id=gateway_id,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "Gateway restart initiated"


def test_gateway_upgrade(mock_client, mock_responses):
    """Test upgrading a gateway."""
    # Mock the gateway upgrade endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.GATEWAY_UPGRADE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Gateway upgrade initiated",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.gateway_upgrade(
        gateway_id="gateway123",
        store_id="store123",
        firmware_version="v2.1"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "gateway123" in request_body
    assert "store123" in request_body
    assert "v2.1" in request_body
    
    # Verify the result
    assert result == "Gateway upgrade initiated"