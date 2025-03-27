"""
Main client class for interacting with the Minew API.
"""
from typing import Dict, List, Optional, Any, Union

from .base import BaseClient
from .resources.store import StoreResource
from .resources.gateway import GatewayResource
from .resources.label import LabelResource
from .resources.template import TemplateResource
from .resources.data import DataResource


class MinewAPIClient:
    """
    Main client class to interact with Minew API.
    Handles authentication, token management, and request dispatch through
    resource-specific classes.
    """
    
    def __init__(self, username: str, password: str, base_url: Optional[str] = None):
        """
        Initialize the client with credentials.
        
        Args:
            username (str): User's username
            password (str): User's password
            base_url (str, optional): API base URL. Defaults to None.
        """
        # Initialize the base client
        self._base_client = BaseClient(username, password, base_url)
        
        # Initialize resource handlers
        self._store = StoreResource(self._base_client)
        self._gateway = GatewayResource(self._base_client)
        self._label = LabelResource(self._base_client)
        self._template = TemplateResource(self._base_client)
        self._data = DataResource(self._base_client)

    @property
    def token(self) -> Optional[str]:
        """Get the current authentication token."""
        return self._base_client.token
    
    @property
    def base_url(self) -> str:
        """Get the base URL used for API requests."""
        return self._base_client.base_url

    # Store API Methods
    def store_add(self, number: str, name: str, address: str) -> str:
        """
        Creates a new store.
        
        Args:
            number (str): Unique store identifier
            name (str): Store's name
            address (str): Store's address
            
        Returns:
            str: New store ID
        """
        return self._store.add(number, name, address)
    
    def store_modify(self, id: str, name: str, address: str, active: int) -> str:
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
        return self._store.modify(id, name, address, active)
    
    def store_close_or_open(self, id: str, active: int) -> str:
        """
        Closes or opens a store.
        
        Args:
            id (str): Store's ID
            active (int): 1 to open the store, 0 to close the store
            
        Returns:
            str: API response indicating success of the operation
        """
        return self._store.close_or_open(id, active)
    
    def store_get_information(
        self, active: int = 1, condition: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves information about stores based on active status or condition.
        
        Args:
            active (int): 1 to get active stores, 0 for inactive stores
            condition (str, optional): Optional store name, number, or address
                to filter results
                
        Returns:
            List[Dict[str, Any]]: API response containing store information
        """
        return self._store.get_information(active, condition)
    
    def store_get_warnings(self, store_id: str, screening: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves warning information for a specific store.
        
        Args:
            store_id (str): The store's ID
            screening (str, optional): 'brush' for brush warnings, 'upgrade'
                for upgrade warnings
                
        Returns:
            Dict[str, Any]: API response containing warning details
        """
        return self._store.get_warnings(store_id, screening)
    
    def store_get_logs(
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
        return self._store.get_logs(
            store_id, current_page, page_size, object_type, action_type, condition
        )
    
    # Gateway API Methods
    def gateway_add(self, mac: str, name: str, store_id: str) -> str:
        """
        Adds a new gateway to the store.
        
        Args:
            mac (str): Gateway MAC address
            name (str): Gateway name
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._gateway.add(mac, name, store_id)
    
    def gateway_delete(self, gateway_id: str, store_id: str) -> str:
        """
        Deletes a gateway from the store.
        
        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._gateway.delete(gateway_id, store_id)
    
    def gateway_list(self, store_id: str, page: int, size: int) -> List[Dict[str, Any]]:
        """
        Retrieves the list of gateways for a store.
        
        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            
        Returns:
            List[Dict[str, Any]]: List of gateway information
        """
        return self._gateway.list(store_id, page, size)
    
    def gateway_modify(self, gateway_id: str, name: str) -> str:
        """
        Modifies the information of a gateway.
        
        Args:
            gateway_id (str): Gateway ID or MAC address
            name (str): Gateway name
            
        Returns:
            str: Success message from the API
        """
        return self._gateway.modify(gateway_id, name)
    
    def gateway_restart(self, gateway_id: str, store_id: str) -> str:
        """
        Restarts a specific gateway.
        
        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._gateway.restart(gateway_id, store_id)
    
    def gateway_upgrade(self, gateway_id: str, store_id: str, firmware_version: str) -> str:
        """
        Upgrades gateway firmware.
        
        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID
            firmware_version (str): Firmware version to upgrade to
            
        Returns:
            str: Success message from the API
        """
        return self._gateway.upgrade(gateway_id, store_id, firmware_version)
    
    # Label API Methods
    def label_add(self, mac: str, store_id: str, demo_name: str) -> str:
        """
        Adds a new label to the system.
        
        Args:
            mac (str): Label MAC address
            store_id (str): Store ID
            demo_name (str): Template name to be used
            
        Returns:
            str: Label ID if successful
        """
        return self._label.add(mac, store_id, demo_name)
    
    def label_list(self, store_id: str, page: int, size: int, condition: Optional[str] = None) -> Dict[str, Any]:
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
        return self._label.list(store_id, page, size, condition)
    
    def label_delete(self, label_id: str, store_id: str) -> str:
        """
        Deletes a label from the system.
        
        Args:
            label_id (str): Label ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._label.delete(label_id, store_id)
    
    def label_update(self, label_id: str, name: str) -> str:
        """
        Updates an existing label's information.
        
        Args:
            label_id (str): Label ID
            name (str): New label name
            
        Returns:
            str: Success message from the API
        """
        return self._label.update(label_id, name)
    
    def label_binding(self, label_id: str, data_id: str, store_id: str) -> str:
        """
        Binds a label to a product/data item.
        
        Args:
            label_id (str): Label ID
            data_id (str): Data/Product ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._label.binding(label_id, data_id, store_id)
    
    def label_refresh(self, label_ids: List[str], store_id: str) -> str:
        """
        Refreshes the display of one or more labels.
        
        Args:
            label_ids (List[str]): List of label IDs to refresh
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._label.refresh(label_ids, store_id)
    
    def label_unbinding(self, label_id: str, store_id: str) -> str:
        """
        Unbinds a label from its product/data association.
        
        Args:
            label_id (str): Label ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._label.unbinding(label_id, store_id)
    
    def label_upgrade(self, label_ids: List[str], store_id: str, firmware_version: str) -> str:
        """
        Upgrades label firmware.
        
        Args:
            label_ids (List[str]): List of label IDs to upgrade
            store_id (str): Store ID
            firmware_version (str): Firmware version to upgrade to
            
        Returns:
            str: Success message from the API
        """
        return self._label.upgrade(label_ids, store_id, firmware_version)
    
    def label_find_by_mac(self, mac: str, store_id: str) -> Dict[str, Any]:
        """
        Finds a label by its MAC address.
        
        Args:
            mac (str): Label MAC address
            store_id (str): Store ID
            
        Returns:
            Dict[str, Any]: Label information
        """
        return self._label.find_by_mac(mac, store_id)
    
    def label_flash(self, label_id: str, store_id: str, flash_mode: int) -> str:
        """
        Flashes the label LED for visual identification.
        
        Args:
            label_id (str): Label ID
            store_id (str): Store ID
            flash_mode (int): LED flash mode (e.g., 1 for flashing, 0 for static)
            
        Returns:
            str: Success message from the API
        """
        return self._label.flash(label_id, store_id, flash_mode)
    
    # Template API Methods
    def template_list(
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
        return self._template.list(
            store_id, page, size, screening, inch, color, fuzzy
        )
    
    def template_preview_unbound(self, demo_name: str) -> str:
        """
        Previews a template that is not bound to any data.
        
        Args:
            demo_name (str): Template name
            
        Returns:
            str: API response containing the image preview in base64 format
        """
        return self._template.preview_unbound(demo_name)
    
    def template_preview_bound(self, demo_name: str, data_id: str, store_id: str) -> str:
        """
        Previews a template bound to specific data.
        
        Args:
            demo_name (str): Template name
            data_id (str): Data/Product ID
            store_id (str): Store ID
            
        Returns:
            str: API response containing the image preview in base64 format
        """
        return self._template.preview_bound(demo_name, data_id, store_id)
    
    def template_add(self, store_id: str, template_name: str, content: str) -> str:
        """
        Adds a new template to the system.
        
        Args:
            store_id (str): Store ID
            template_name (str): Template name
            content (str): Template content
            
        Returns:
            str: Template ID if successful
        """
        return self._template.add(store_id, template_name, content)
    
    def template_update(self, template_id: str, store_id: str, template_name: str, content: str) -> str:
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
        return self._template.update(template_id, store_id, template_name, content)
    
    def template_delete(self, template_id: str, store_id: str) -> str:
        """
        Deletes a template from the system.
        
        Args:
            template_id (str): Template ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._template.delete(template_id, store_id)
    
    # Data API Methods
    def data_add(self, store_id: str, product_data: Dict[str, Any]) -> str:
        """
        Adds product data to the system.
        
        Args:
            store_id (str): Store ID
            product_data (Dict[str, Any]): Dictionary containing product information
            
        Returns:
            str: Data ID if successful
        """
        return self._data.add(store_id, product_data)
    
    def data_update(self, data_id: str, store_id: str, product_data: Dict[str, Any]) -> str:
        """
        Updates existing product data.
        
        Args:
            data_id (str): Data ID
            store_id (str): Store ID
            product_data (Dict[str, Any]): Dictionary containing updated product information
            
        Returns:
            str: Success message from the API
        """
        return self._data.update(data_id, store_id, product_data)
    
    def data_delete(self, data_id: str, store_id: str) -> str:
        """
        Deletes product data from the system.
        
        Args:
            data_id (str): Data ID
            store_id (str): Store ID
            
        Returns:
            str: Success message from the API
        """
        return self._data.delete(data_id, store_id)
    
    def data_list(self, store_id: str, page: int, size: int, condition: Optional[str] = None) -> Dict[str, Any]:
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
        return self._data.list(store_id, page, size, condition)
    
    def data_binding_list(self, store_id: str, page: int, size: int) -> Dict[str, Any]:
        """
        Gets a list of data items bound to labels.
        
        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            
        Returns:
            Dict[str, Any]: Dictionary containing bound data information and pagination details
        """
        return self._data.binding_list(store_id, page, size)