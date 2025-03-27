"""
Product data management resources.
"""
from typing import Dict, List, Optional, Any

from ..base import BaseResource


class DataResource(BaseResource):
    """
    Resource for managing product data.
    """
    DATA_ADD_ENDPOINT = "/esl/data/add"
    DATA_UPDATE_ENDPOINT = "/esl/data/update"
    DATA_DELETE_ENDPOINT = "/esl/data/delete"
    DATA_LIST_ENDPOINT = "/esl/data/list"
    DATA_BINDING_LIST_ENDPOINT = "/esl/data/bindingList"

    def add(self, store_id: str, product_data: Dict[str, Any]) -> str:
        """
        Adds product data to the system.

        Args:
            store_id (str): Store ID
            product_data (Dict[str, Any]): Dictionary containing product information

        Returns:
            str: Data ID if successful
        """
        data = {
            "storeId": store_id,
            **product_data
        }

        response = self.client.post(self.DATA_ADD_ENDPOINT, data)

        response, _, _ = self.client.parse_response(
            response,
            "Data add failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("dataId", "")

    def update(self, data_id: str, store_id: str, product_data: Dict[str, Any]) -> str:
        """
        Updates existing product data.

        Args:
            data_id (str): Data ID
            store_id (str): Store ID
            product_data (Dict[str, Any]): Dictionary containing updated product information

        Returns:
            str: Success message from the API
        """
        data = {
            "id": data_id,
            "storeId": store_id,
            **product_data
        }

        response = self.client.put(self.DATA_UPDATE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Data update failed: Code: {code} - Message: {msg}"
        )

        return msg

    def delete(self, data_id: str, store_id: str) -> str:
        """
        Deletes product data from the system.

        Args:
            data_id (str): Data ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        params = {
            "id": data_id,
            "storeId": store_id
        }

        response = self.client.get(self.DATA_DELETE_ENDPOINT, params)

        _, _, msg = self.client.parse_response(
            response,
            "Data delete failed: Code: {code} - Message: {msg}"
        )

        return msg

    def list(self, store_id: str, page: int, size: int, condition: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves a list of product data items.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            condition (str, optional): Filter condition (e.g., product name)

        Returns:
            Dict[str, Any]: Dictionary containing product data information and pagination details
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        if condition:
            params["condition"] = condition

        response = self.client.get(self.DATA_LIST_ENDPOINT, params)

        response, _, _ = self.client.parse_response(
            response,
            "Data list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response

    def binding_list(self, store_id: str, page: int, size: int) -> Dict[str, Any]:
        """
        Gets a list of data items bound to labels.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page

        Returns:
            Dict[str, Any]: Dictionary containing bound data information and pagination details
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        response = self.client.get(self.DATA_BINDING_LIST_ENDPOINT, params)

        response, _, _ = self.client.parse_response(
            response,
            "Data binding list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response