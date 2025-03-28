"""
Tests for template and data management endpoints of the MinewAPIClient.
"""
import pytest
import responses
from minew_api.client import MinewAPIClient
from minew_api.exceptions import APIError


# Template Endpoint Tests
def test_template_list(mock_client, mock_responses):
    """Test listing templates."""
    store_id = "store123"
    page = 1
    size = 10
    screening = 0
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}&screening={screening}",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "rows": [
                    {
                        "id": "template1",
                        "name": "Template 1",
                        "size": "2.13",
                        "color": "BWR"
                    },
                    {
                        "id": "template2",
                        "name": "Template 2",
                        "size": "2.9",
                        "color": "BWR"
                    }
                ]
            }
        },
        status=200
    )
    
    # Call the method
    templates = mock_client.template_list(
        store_id=store_id,
        page=page,
        size=size,
        screening=screening
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert len(templates) == 2
    assert templates[0]["id"] == "template1"
    assert templates[1]["name"] == "Template 2"
    
    # Test with optional parameters
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}&screening={screening}&inch=2.13&color=BWR&fuzzy=sales",
        json={
            "code": 200,
            "msg": "success",
            "data": {"rows": [{"id": "template1"}]}
        },
        status=200
    )
    
    templates = mock_client.template_list(
        store_id=store_id,
        page=page,
        size=size,
        screening=screening,
        inch=2.13,
        color="BWR",
        fuzzy="sales"
    )
    
    assert len(mock_responses.calls) == 2


def test_template_preview_unbound(mock_client, mock_responses):
    """Test previewing an unbound template."""
    # Mock the template preview unbound endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_PREVIEW_UNBOUND_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": "base64encodedimagedata"
        },
        status=200
    )
    
    # Call the method
    preview = mock_client.template_preview_unbound(
        demo_name="Template 1"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "Template 1" in request_body
    
    # Verify the result
    assert preview == "base64encodedimagedata"


def test_template_preview_bound(mock_client, mock_responses):
    """Test previewing a bound template."""
    # Mock the template preview bound endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_PREVIEW_BOUND_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": "base64encodedimagedata"
        },
        status=200
    )
    
    # Call the method
    preview = mock_client.template_preview_bound(
        demo_name="Template 1",
        data_id="data123",
        store_id="store123"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "Template 1" in request_body
    assert "data123" in request_body
    assert "store123" in request_body
    
    # Verify the result
    assert preview == "base64encodedimagedata"


def test_template_add(mock_client, mock_responses):
    """Test adding a template."""
    # Mock the template add endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_ADD_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {"templateId": "template123"}
        },
        status=200
    )
    
    # Call the method
    template_id = mock_client.template_add(
        store_id="store123",
        template_name="New Template",
        content="template content data"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "store123" in request_body
    assert "New Template" in request_body
    assert "template content data" in request_body
    
    # Verify the result
    assert template_id == "template123"


def test_template_update(mock_client, mock_responses):
    """Test updating a template."""
    # Mock the template update endpoint
    mock_responses.add(
        responses.PUT,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_UPDATE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Template updated successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.template_update(
        template_id="template123",
        store_id="store123",
        template_name="Updated Template",
        content="updated content data"
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "template123" in request_body
    assert "store123" in request_body
    assert "Updated Template" in request_body
    assert "updated content data" in request_body
    
    # Verify the result
    assert result == "Template updated successfully"


def test_template_delete(mock_client, mock_responses):
    """Test deleting a template."""
    # Mock the template delete endpoint
    template_id = "template123"
    store_id = "store123"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.TEMPLATE_DELETE_ENDPOINT}?id={template_id}&storeId={store_id}",
        json={
            "code": 200,
            "msg": "Template deleted successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.template_delete(
        template_id=template_id,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "Template deleted successfully"


# Data Endpoint Tests
def test_data_add(mock_client, mock_responses):
    """Test adding product data."""
    # Mock the data add endpoint
    mock_responses.add(
        responses.POST,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.DATA_ADD_ENDPOINT}",
        json={
            "code": 200,
            "msg": "success",
            "data": {"dataId": "data123"}
        },
        status=200
    )
    
    # Call the method
    data_id = mock_client.data_add(
        store_id="store123",
        product_data={
            "name": "Test Product",
            "price": "9.99",
            "sku": "SKU123",
            "barcode": "123456789012"
        }
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "store123" in request_body
    assert "Test Product" in request_body
    assert "9.99" in request_body
    assert "SKU123" in request_body
    
    # Verify the result
    assert data_id == "data123"


def test_data_update(mock_client, mock_responses):
    """Test updating product data."""
    # Mock the data update endpoint
    mock_responses.add(
        responses.PUT,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.DATA_UPDATE_ENDPOINT}",
        json={
            "code": 200,
            "msg": "Data updated successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.data_update(
        data_id="data123",
        store_id="store123",
        product_data={
            "name": "Updated Product",
            "price": "10.99",
            "sku": "SKU123",
            "barcode": "123456789012"
        }
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    request_body = mock_responses.calls[0].request.body.decode()
    assert "data123" in request_body
    assert "store123" in request_body
    assert "Updated Product" in request_body
    assert "10.99" in request_body
    
    # Verify the result
    assert result == "Data updated successfully"


def test_data_delete(mock_client, mock_responses):
    """Test deleting product data."""
    # Mock the data delete endpoint
    data_id = "data123"
    store_id = "store123"
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.DATA_DELETE_ENDPOINT}?id={data_id}&storeId={store_id}",
        json={
            "code": 200,
            "msg": "Data deleted successfully",
            "data": None
        },
        status=200
    )
    
    # Call the method
    result = mock_client.data_delete(
        data_id=data_id,
        store_id=store_id
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert result == "Data deleted successfully"


def test_data_list(mock_client, mock_responses):
    """Test listing product data."""
    # Mock the data list endpoint
    store_id = "store123"
    page = 1
    size = 10
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.DATA_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "items": [
                    {
                        "id": "data1",
                        "name": "Product 1",
                        "price": "9.99",
                        "sku": "SKU1"
                    },
                    {
                        "id": "data2",
                        "name": "Product 2",
                        "price": "19.99",
                        "sku": "SKU2"
                    }
                ]
            }
        },
        status=200
    )
    
    # Call the method
    result = mock_client.data_list(
        store_id=store_id,
        page=page,
        size=size
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert "items" in result["data"]
    assert len(result["data"]["items"]) == 2
    assert result["data"]["items"][0]["name"] == "Product 1"
    assert result["data"]["items"][1]["price"] == "19.99"
    
    # Test with condition
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.DATA_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}&condition=Product",
        json={
            "code": 200,
            "msg": "success",
            "data": {"items": [{"id": "data1", "name": "Product 1"}]}
        },
        status=200
    )
    
    result = mock_client.data_list(
        store_id=store_id,
        page=page,
        size=size,
        condition="Product"
    )
    
    assert len(mock_responses.calls) == 2


def test_data_binding_list(mock_client, mock_responses):
    """Test listing bound data items."""
    # Mock the data binding list endpoint
    store_id = "store123"
    page = 1
    size = 10
    
    mock_responses.add(
        responses.GET,
        f"{MinewAPIClient.BASE_URL}{MinewAPIClient.DATA_BINDING_LIST_ENDPOINT}?storeId={store_id}&page={page}&size={size}",
        json={
            "code": 200,
            "msg": "success",
            "data": {
                "items": [
                    {
                        "dataId": "data1",
                        "labelId": "label1",
                        "productName": "Product 1",
                        "labelMac": "AC233FC03CEC"
                    },
                    {
                        "dataId": "data2",
                        "labelId": "label2",
                        "productName": "Product 2",
                        "labelMac": "AC233FC03CED"
                    }
                ]
            }
        },
        status=200
    )
    
    # Call the method
    result = mock_client.data_binding_list(
        store_id=store_id,
        page=page,
        size=size
    )
    
    # Verify the request
    assert len(mock_responses.calls) == 1
    
    # Verify the result
    assert "items" in result["data"]
    assert len(result["data"]["items"]) == 2
    assert result["data"]["items"][0]["dataId"] == "data1"
    assert result["data"]["items"][1]["labelId"] == "label2"