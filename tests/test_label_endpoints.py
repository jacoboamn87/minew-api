"""
Tests for label management endpoints of the MinewAPIClient.
"""
import pytest
import responses
from minew_api.client import MinewAPIClient
from minew_api.exceptions import APIError


def test_label_add(mock_client, mock_responses):
    """Test adding a new label."""
    # Mock the label add endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_ADD_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {"labelId": "label123"}
        },
        status=200
    )
    
    # Call the method
    label_id = mock_client.label_add(
        mac="AC233FC03CEC",
        store_id="store123",
        demo_name="template1"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "AC233FC03CEC" in request_body
    assert "store123" in request_body
    assert "template1" in request_body
    
    # Verify the result
    assert label_id == "label123"


def test_label_list(mock_client, mock_responses):
    """Test listing labels."""
    # Mock the label list endpoint
    store_id = "store123"
    page = 1
    size = 10
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "currentPage": 1,
                "pageSize": 10,
                "totalNum": 2,
                "isMore": 0,
                "totalPage": 1,
                "items": [
                    {
                        "id": "label1",
                        "mac": "AC233FC03CEC",
                        "name": "Label 1",
                        "status": 1
                    },
                    {
                        "id": "label2",
                        "mac": "AC233FC03CED",
                        "name": "Label 2",
                        "status": 1
                    }
                ]
            }
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_list(
        store_id=store_id,
        page=page,
        size=size
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result["data"]["items"][0]["id"] == "label1"
    assert result["data"]["items"][1]["mac"] == "AC233FC03CED"
    
    # Test with condition
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}&condition=Label",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "items": [{"id": "label1", "name": "Label 1"}]
            }
        },
        status=200
    )
    
    result = mock_client.label_list(
        store_id=store_id,
        page=page,
        size=size,
        condition="Label"
    )
    
    assert len(mock_responses.calls) == 2


def test_label_delete(mock_client, mock_responses):
    """Test deleting a label."""
    # Mock the label delete endpoint
    label_id = "label123"
    store_id = "store123"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_DELETE_ENDPOINT}?id={label_id}&storeId={store_id}",
        json={
            "code": 200,
            "msg": "Label deleted successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_delete(
        label_id=label_id,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "Label deleted successfully"


def test_label_update(mock_client, mock_responses):
    """Test updating a label."""
    # Mock the label update endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_UPDATE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Label updated successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_update(
        label_id="label123",
        name="New Label Name"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "label123" in request_body
    assert "New Label Name" in request_body
    
    # Verify the result
    assert result == "Label updated successfully"


def test_label_binding(mock_client, mock_responses):
    """Test binding a label to data."""
    # Mock the label binding endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_BINDING_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Label bound successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_binding(
        label_id="label123",
        data_id="data123",
        store_id="store123"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "label123" in request_body
    assert "data123" in request_body
    assert "store123" in request_body
    
    # Verify the result
    assert result == "Label bound successfully"


def test_label_refresh(mock_client, mock_responses):
    """Test refreshing labels."""
    # Mock the label refresh endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_REFRESH_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Labels refreshed successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_refresh(
        label_ids=["label123", "label456"],
        store_id="store123"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "label123" in request_body
    assert "label456" in request_body
    assert "store123" in request_body
    
    # Verify the result
    assert result == "Labels refreshed successfully"


def test_label_unbinding(mock_client, mock_responses):
    """Test unbinding a label."""
    # Mock the label unbinding endpoint
    label_id = "label123"
    store_id = "store123"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_UNBINDING_ENDPOINT}?labelId={label_id}&storeId={store_id}",
        json={
            "code": 200,
            "msg": "Label unbound successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_unbinding(
        label_id=label_id,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "Label unbound successfully"


def test_label_upgrade(mock_client, mock_responses):
    """Test upgrading label firmware."""
    # Mock the label upgrade endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_UPGRADE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Label upgrade initiated",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_upgrade(
        label_ids=["label123", "label456"],
        store_id="store123",
        firmware_version="v2.1"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "label123" in request_body
    assert "label456" in request_body
    assert "store123" in request_body
    assert "v2.1" in request_body
    
    # Verify the result
    assert result == "Label upgrade initiated"


def test_label_find_by_mac(mock_client, mock_responses):
    """Test finding a label by MAC address."""
    # Mock the label find by MAC endpoint
    mac = "AC233FC03CEC"
    store_id = "store123"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_FIND_BY_MAC_ENDPOINT}?mac={mac}&storeId={store_id}",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "id": "label123",
                "mac": mac,
                "name": "Label 1",
                "status": 1
            }
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_find_by_mac(
        mac=mac,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result["id"] == "label123"
    assert result["mac"] == mac


def test_label_flash(mock_client, mock_responses):
    """Test flashing a label's LED."""
    # Mock the label flash endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.LABEL_FLASH_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Label flash initiated",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.label_flash(
        label_id="label123",
        store_id="store123",
        flash_mode=1
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "label123" in request_body
    assert "store123" in request_body
    assert "1" in request_body
    
    # Verify the result
    assert result == "Label flash initiated"