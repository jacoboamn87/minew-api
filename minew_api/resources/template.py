"""
Template management resources.
"""
from typing import Dict, List, Optional, Any, Union

from ..base import BaseResource


class TemplateResource(BaseResource):
    """
    Resource for managing ESL templates.
    """
    TEMPLATE_LIST_ENDPOINT = "/esl/template/findAll"
    TEMPLATE_PREVIEW_UNBOUND_ENDPOINT = "/esl/template/previewTemplate"
    TEMPLATE_PREVIEW_BOUND_ENDPOINT = "/esl/template/preview"
    TEMPLATE_ADD_ENDPOINT = "/esl/template/add"
    TEMPLATE_UPDATE_ENDPOINT = "/esl/template/update"
    TEMPLATE_DELETE_ENDPOINT = "/esl/template/delete"

    def list(
        self,
        store_id: str,
        page: int,
        size: int,
        screening: int = 0,
        inch: Optional[float] = None,
        color: Optional[str] = None,
        fuzzy: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Queries the list of templates for a store.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            screening (int, optional):
                0 for all templates, 1 for system templates,
                others for store templates
            inch (float, optional): Template size in inches
            color (str, optional): Template color
            fuzzy (str, optional): Fuzzy query filter for templates

        Returns:
            List[Dict[str, Any]]: API response containing templates information
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size,
            "screening": screening,
        }

        if inch:
            params["inch"] = inch
        if color:
            params["color"] = color
        if fuzzy:
            params["fuzzy"] = fuzzy

        response = self.client.get(self.TEMPLATE_LIST_ENDPOINT, params)

        response, _, _ = self.client.parse_response(
            response,
            "Template list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("rows", [])

    def preview_unbound(self, demo_name: str) -> str:
        """
        Previews a template that is not bound to any data.

        Args:
            demo_name (str): Template name

        Returns:
            str: API response containing the image preview in base64 format
        """
        data = {"demoName": demo_name}

        response = self.client.post(self.TEMPLATE_PREVIEW_UNBOUND_ENDPOINT, data)

        response, _, _ = self.client.parse_response(
            response,
            "Template unbound preview failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", "")

    def preview_bound(self, demo_name: str, data_id: str, store_id: str) -> str:
        """
        Previews a template bound to specific data.

        Args:
            demo_name (str): Template name
            data_id (str): Data/Product ID
            store_id (str): Store ID

        Returns:
            str: API response containing the image preview in base64 format
        """
        data = {"demoName": demo_name, "id": data_id, "storeId": store_id}

        response = self.client.post(self.TEMPLATE_PREVIEW_BOUND_ENDPOINT, data)

        response, _, _ = self.client.parse_response(
            response,
            "Template bound preview failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", "")

    def add(self, store_id: str, template_name: str, content: str) -> str:
        """
        Adds a new template to the system.

        Args:
            store_id (str): Store ID
            template_name (str): Template name
            content (str): Template content

        Returns:
            str: Template ID if successful
        """
        data = {
            "storeId": store_id,
            "templateName": template_name,
            "content": content
        }

        response = self.client.post(self.TEMPLATE_ADD_ENDPOINT, data)

        response, _, _ = self.client.parse_response(
            response,
            "Template add failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("templateId", "")

    def update(self, template_id: str, store_id: str, template_name: str, content: str) -> str:
        """
        Updates an existing template.

        Args:
            template_id (str): Template ID
            store_id (str): Store ID
            template_name (str): Updated template name
            content (str): Updated template content

        Returns:
            str: Success message from the API
        """
        data = {
            "id": template_id,
            "storeId": store_id,
            "templateName": template_name,
            "content": content
        }

        response = self.client.put(self.TEMPLATE_UPDATE_ENDPOINT, data)

        _, _, msg = self.client.parse_response(
            response,
            "Template update failed: Code: {code} - Message: {msg}"
        )

        return msg

    def delete(self, template_id: str, store_id: str) -> str:
        """
        Deletes a template from the system.

        Args:
            template_id (str): Template ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API
        """
        params = {
            "id": template_id,
            "storeId": store_id
        }

        response = self.client.get(self.TEMPLATE_DELETE_ENDPOINT, params)

        _, _, msg = self.client.parse_response(
            response,
            "Template delete failed: Code: {code} - Message: {msg}"
        )

        return msg