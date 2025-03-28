"""
Label management resources.
"""
from typing import Dict, List, Optional, Any, Union

from ..base import BaseResource


class LabelResource(BaseResource):
    """
    Resource for managing ESL labels.
    """
    LABEL_ADD_ENDPOINT = "/esl/label/add"
    LABEL_LIST_ENDPOINT = "/esl/label/list"
    LABEL_DELETE_ENDPOINT = "/esl/label/delete"
    LABEL_UPDATE_ENDPOINT = "/esl/label/update"
    LABEL_BINDING_ENDPOINT = "/esl/label/binding"
    LABEL_REFRESH_ENDPOINT = "/esl/label/refresh"
    LABEL_UNBINDING_ENDPOINT = "/esl/label/unbinding"
    LABEL_UPGRADE_ENDPOINT = "/esl/label/upgrade"
    LABEL_FIND_BY_MAC_ENDPOINT = "/esl/label/findByMac"
    LABEL_FLASH_ENDPOINT = "/esl/label/flash"

    def add(self, mac: str, store_id: str, demo_name: str) -> str:
        """
        Adds a new label to the system.

        Args:
            mac (str): Label MAC address
            store_id (str): Store ID
            demo_name (str): Template name to be used

        Returns:
            str: Label ID if successful
        """
        data = {
            "mac": mac,
            "storeId": store_id,
            "demoName": demo_name
        }

        response = self.client.post(self.LABEL_ADD_ENDPOINT, data)

        response_data, _, _ = self.client.parse_response(
            response,
            "Label add failed: Code: {code} - Message: {msg}"
        )

        data_dict = response_data.get("data", {})
        if isinstance(data_dict, dict):
            return data_dict.get("labelId", "")
        return ""

    def list(self, store_id: str, page: int, size: int, condition: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves a list of labels in a store.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            condition (str, optional): Filter condition (e.g., label MAC or name)

        Returns:
            Dict[str, Any]: Dictionary containing label information and pagination details
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        if condition:
            params["condition"] = condition

        response = self.client.get(self.LABEL_LIST_ENDPOINT, params)

        response_data, _, _ = self.client.parse_response(
            response,
            "Label list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response_data

    def delete(self, label_id: str, store_id: str) -> str:
        """
        Deletes a label from the system.

        Args:
            label_id (str): Label ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        params = {
            "id": label_id,
            "storeId": store_id
        }

        response = self.client.get(self.LABEL_DELETE_ENDPOINT, params)

        _, _, msg = self.client.parse_response(
            response,
            "Label delete failed: Code: {code} - Message: {msg}"
        )

        return msg

    def update(self, label_id: str, name: str) -> str:
        """
        Updates an existing label's information.

        Args:
            label_id (str): Label ID
            name (str): New label name

        Returns:
            str: Success message from the API
        """
        data = {
            "id": label_id,
            "name": name
        }

        response = self.client.post(self.LABEL_UPDATE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Label update failed: Code: {code} - Message: {msg}"
        )

        return msg

    def binding(self, label_id: str, data_id: str, store_id: str) -> str:
        """
        Binds a label to a product/data item.

        Args:
            label_id (str): Label ID
            data_id (str): Data/Product ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        data = {
            "labelId": label_id,
            "dataId": data_id,
            "storeId": store_id
        }

        response = self.client.post(self.LABEL_BINDING_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Label binding failed: Code: {code} - Message: {msg}"
        )

        return msg

    def refresh(self, label_ids: List[str], store_id: str) -> str:
        """
        Refreshes the display of one or more labels.

        Args:
            label_ids (List[str]): List of label IDs to refresh
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        data = {
            "labelIds": label_ids,
            "storeId": store_id
        }

        response = self.client.post(self.LABEL_REFRESH_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Label refresh failed: Code: {code} - Message: {msg}"
        )

        return msg

    def unbinding(self, label_id: str, store_id: str) -> str:
        """
        Unbinds a label from its product/data association.

        Args:
            label_id (str): Label ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        params = {
            "labelId": label_id,
            "storeId": store_id
        }

        response = self.client.get(self.LABEL_UNBINDING_ENDPOINT, params)

        _, _, msg = self.client.parse_response(
            response,
            "Label unbinding failed: Code: {code} - Message: {msg}"
        )

        return msg

    def upgrade(self, label_ids: List[str], store_id: str, firmware_version: str) -> str:
        """
        Upgrades label firmware.

        Args:
            label_ids (List[str]): List of label IDs to upgrade
            store_id (str): Store ID
            firmware_version (str): Firmware version to upgrade to

        Returns:
            str: Success message from the API
        """
        data = {
            "labelIds": label_ids,
            "storeId": store_id,
            "firmwareVersion": firmware_version
        }

        response = self.client.post(self.LABEL_UPGRADE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Label upgrade failed: Code: {code} - Message: {msg}"
        )

        return msg

    def find_by_mac(self, mac: str, store_id: str) -> Dict[str, Any]:
        """
        Finds a label by its MAC address.

        Args:
            mac (str): Label MAC address
            store_id (str): Store ID

        Returns:
            Dict[str, Any]: Label information
        """
        params = {
            "mac": mac,
            "storeId": store_id
        }

        response = self.client.get(self.LABEL_FIND_BY_MAC_ENDPOINT, params)

        response_data, _, _ = self.client.parse_response(
            response,
            "Label find by MAC failed: Code: {code} - Message: {msg}"
        )

        data_dict = response_data.get("data", {})
        if isinstance(data_dict, dict):
            return data_dict
        return {}

    def flash(self, label_id: str, store_id: str, flash_mode: int) -> str:
        """
        Flashes the label LED for visual identification.

        Args:
            label_id (str): Label ID
            store_id (str): Store ID
            flash_mode (int): LED flash mode (e.g., 1 for flashing, 0 for static)

        Returns:
            str: Success message from the API
        """
        data = {
            "labelId": label_id,
            "storeId": store_id,
            "flashMode": flash_mode
        }

        response = self.client.post(self.LABEL_FLASH_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Label flash failed: Code: {code} - Message: {msg}"
        )

        return msg

