"""
Store management resources.
"""
from typing import Dict, List, Optional, Any, Union

from ..base import BaseResource


class StoreResource(BaseResource):
    """
    Resource for managing stores.
    """
    STORE_ADD_ENDPOINT = "/esl/store/add"
    STORE_UPDATE_ENDPOINT = "/esl/store/update"
    STORE_ACTIVE_ENDPOINT = "/esl/store/openOrClose"
    STORE_LIST_ENDPOINT = "/esl/store/list"
    STORE_WARNING_ENDPOINT = "/esl/warning/findAllWarnings"
    STORE_LOGS_ENDPOINT = "/esl/logs/queryList"

    def add(self, number: str, name: str, address: str) -> str:
        """
        Creates a new store and returns its ID.

        Args:
            number (str): Unique store identifier
            name (str): Store's name
            address (str): Store's address

        Returns:
            str: API response new store ID
        """
        data = {"number": number, "name": name, "address": address}

        response = self.client.post(self.STORE_ADD_ENDPOINT, data)

        response, _, _ = self.client.parse_response(
            response,
            "Store creation failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("storeId")

    def modify(self, id: str, name: str, address: str, active: int) -> str:
        """
        Modifies an existing store's details.

        Args:
            id (str): Store's ID
            name (str): Updated name of the store
            address (str): Updated address of the store
            active (int): Status of the store (1 for active, 0 for inactive)

        Returns:
            str: API response containing the status of the update operation
        """
        data = {"id": id, "name": name, "address": address, "active": active}

        response = self.client.put(self.STORE_UPDATE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Store modification failed: Code: {code} - Message: {msg}"
        )

        return msg

    def close_or_open(self, id: str, active: int) -> str:
        """
        Closes or opens a store.

        Args:
            id (str): Store's ID
            active (int): 1 to open the store, 0 to close the store

        Returns:
            str: API response indicating success of the operation
        """
        if active not in [0, 1]:
            raise ValueError("Only `0` or `1` are valid values for `active`.")

        params = {"storeId": id, "active": active}

        response = self.client.get(self.STORE_ACTIVE_ENDPOINT, params)

        _, _, msg = self.client.parse_response(
            response,
            "Store {action} failed: Code: {code} - Message: {msg}"
        )

        return msg

    def get_information(self, active: int = 1, condition: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves information about stores based on active status or condition.

        Args:
            active (int): 1 to get active stores, 0 for inactive stores
            condition (str, optional): Optional store name, number, or address
                to filter results

        Returns:
            List[Dict[str, Any]]: API response containing store information
        """
        params = {"active": active}
        if condition:
            params["condition"] = condition

        response = self.client.get(self.STORE_LIST_ENDPOINT, params)

        response, _, _ = self.client.parse_response(
            response,
            "Retrieving information about stores failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", [])

    def get_warnings(self, store_id: str, screening: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves warning information for a specific store.

        Args:
            store_id (str): The store's ID
            screening (str, optional): 'brush' for brush warnings, 'upgrade'
                for upgrade warnings

        Returns:
            Dict[str, Any]: API response containing warning details
        """
        params = {"storeId": store_id}
        if screening:
            params["screening"] = screening

        response = self.client.get(self.STORE_WARNING_ENDPOINT, params)

        response, _, _ = self.client.parse_response(
            response,
            "Retrieving warning information failed: Code: {code} - Message: {msg}"
        )

        return response

    def get_logs(
        self,
        store_id: str,
        current_page: int,
        page_size: int,
        object_type: str,
        action_type: str = "",
        condition: str = "",
    ) -> Dict[str, Any]:
        """
        Retrieves operation log information for a specific store.

        Args:
            store_id (str): The store's ID
            current_page (int): The current page of the logs
            page_size (int): The number of items per page
            object_type (str): The type of object (1 for label, 5 for warning light)
            action_type (str, optional): Action type (1 for refresh, 2 for upgrade, etc.)
            condition (str, optional): Optional condition for fuzzy search (e.g., mac address)

        Returns:
            Dict[str, Any]: API response containing log information
        """
        data = {
            "storeId": store_id,
            "currentPage": current_page,
            "pageSize": page_size,
            "objectType": object_type,
            "actionType": action_type,
            "condition": condition,
        }

        response = self.client.post(self.STORE_LOGS_ENDPOINT, data)

        response, _, _ = self.client.parse_response(
            response,
            "Retrieving operation log information failed: Code: {code} - Message: {msg}"
        )

        return response