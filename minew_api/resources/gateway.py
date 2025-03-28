"""
Gateway management resources.
"""
from typing import Dict, List, Optional, Any

from ..base import BaseResource


class GatewayResource(BaseResource):
    """
    Resource for managing gateways.
    """
    GATEWAY_ADD_ENDPOINT = "/esl/gateway/add"
    GATEWAY_DELETE_ENDPOINT = "/esl/gateway/delete"
    GATEWAY_LIST_ENDPOINT = "/esl/gateway/listPage"
    GATEWAY_UPDATE_ENDPOINT = "/esl/gateway/update"
    GATEWAY_RESTART_ENDPOINT = "/esl/gateway/restart"
    GATEWAY_UPGRADE_ENDPOINT = "/esl/gateway/upgrade"

    def add(self, mac: str, name: str, store_id: str) -> str:
        """
        Adds a new gateway to the store.

        Args:
            mac (str): Gateway MAC address
            name (str): Gateway name
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        data = {
            "mac": mac,
            "name": name,
            "storeId": store_id
        }

        response = self.client.post(self.GATEWAY_ADD_ENDPOINT, data)

        response_data, _, _ = self.client.parse_response(
            response,
            "Gateway add failed: Code: {code} - Message: {msg}"
        )

        return response_data.get("message", "Success")

    def delete(self, gateway_id: str, store_id: str) -> str:
        """
        Deletes a gateway from the store.

        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        params = {
            "id": gateway_id,
            "storeId": store_id
        }

        response = self.client.get(self.GATEWAY_DELETE_ENDPOINT, params)

        response_data, _, _ = self.client.parse_response(
            response,
            "Gateway delete failed: Code: {code} - Message: {msg}"
        )

        return response_data.get("message", "Success")

    def list(self, store_id: str, page: int, size: int) -> List[Dict[str, Any]]:
        """
        Retrieves the list of gateways for a store.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page

        Returns:
            List[Dict[str, Any]]: List of gateway information
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        response = self.client.get(self.GATEWAY_LIST_ENDPOINT, params)

        response_data, _, _ = self.client.parse_response(
            response,
            "Gateway list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response_data.get("items", [])

    def modify(self, gateway_id: str, name: str) -> str:
        """
        Modifies the information of a gateway.

        Args:
            gateway_id (str): Gateway ID or MAC address
            name (str): Gateway name

        Returns:
            str: Success message from the API
        """
        data = {
            "id": gateway_id,
            "name": name
        }

        response = self.client.post(self.GATEWAY_UPDATE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Gateway modification failed: Code: {code} - Message: {msg}"
        )

        return msg

    def restart(self, gateway_id: str, store_id: str) -> str:
        """
        Restarts a specific gateway.

        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        params = {
            "id": gateway_id,
            "storeId": store_id
        }

        response = self.client.get(self.GATEWAY_RESTART_ENDPOINT, params)

        _, _, msg = self.client.parse_response(
            response,
            "Gateway restart failed: Code: {code} - Message: {msg}"
        )

        return msg

    def upgrade(self, gateway_id: str, store_id: str, firmware_version: str) -> str:
        """
        Upgrades gateway firmware.

        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID
            firmware_version (str): Firmware version to upgrade to

        Returns:
            str: Success message from the API
        """
        data = {
            "gatewayId": gateway_id,
            "storeId": store_id,
            "firmwareVersion": firmware_version
        }

        response = self.client.post(self.GATEWAY_UPGRADE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Gateway upgrade failed: Code: {code} - Message: {msg}"
        )

        return msg

