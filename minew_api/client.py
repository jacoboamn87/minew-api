import hashlib
import requests

from .exceptions import APIError


class MinewAPIClient(object):
    """
    Main client class to interact with Minew API.
    Handles authentication, token management, and request dispatch.
    """

    BASE_URL = "https://cloud.minewtag.com/apis/"
    DATA_ADD_ENDPOINT = "/esl/data/add"
    DATA_BINDING_LIST_ENDPOINT = "/esl/data/bindingList"
    DATA_DELETE_ENDPOINT = "/esl/data/delete"
    DATA_LIST_ENDPOINT = "/esl/data/list"
    DATA_UPDATE_ENDPOINT = "/esl/data/update"
    GATEWAY_ADD_ENDPOINT = "/esl/gateway/add"
    GATEWAY_DELETE_ENDPOINT = "/esl/gateway/delete"
    GATEWAY_LIST_ENDPOINT = "/esl/gateway/listPage"
    GATEWAY_RESTART_ENDPOINT = "/esl/gateway/restart"
    GATEWAY_UPDATE_ENDPOINT = "/esl/gateway/update"
    GATEWAY_UPGRADE_ENDPOINT = "/esl/gateway/upgrade"
    LABEL_ADD_ENDPOINT = "/esl/label/add"
    LABEL_BINDING_ENDPOINT = "/esl/label/binding"
    LABEL_DELETE_ENDPOINT = "/esl/label/delete"
    LABEL_FIND_BY_MAC_ENDPOINT = "/esl/label/findByMac"
    LABEL_FLASH_ENDPOINT = "/esl/label/flash"
    LABEL_LIST_ENDPOINT = "/esl/label/list"
    LABEL_REFRESH_ENDPOINT = "/esl/label/refresh"
    LABEL_UNBINDING_ENDPOINT = "/esl/label/unbinding"
    LABEL_UPDATE_ENDPOINT = "/esl/label/update"
    LABEL_UPGRADE_ENDPOINT = "/esl/label/upgrade"
    LOGIN_ENDPOINT = "/action/login"
    STORE_ACTIVE_ENDPOINT = "/esl/store/openOrClose"
    STORE_ADD_ENDPOINT = "/esl/store/add"
    STORE_LIST_ENDPOINT = "/esl/store/list"
    STORE_LOGS_ENDPOINT = "/esl/logs/queryList"
    STORE_UPDATE_ENDPOINT = "/esl/store/update"
    STORE_WARNING_ENDPOINT = "/esl/warning/findAllWarnings"
    TEMPLATE_ADD_ENDPOINT = "/esl/template/add"
    TEMPLATE_DELETE_ENDPOINT = "/esl/template/delete"
    TEMPLATE_LIST_ENDPOINT = "/esl/template/findAll"
    TEMPLATE_PREVIEW_BOUND_ENDPOINT = "/esl/template/preview"
    TEMPLATE_PREVIEW_UNBOUND_ENDPOINT = "/esl/template/previewTemplate"
    TEMPLATE_UPDATE_ENDPOINT = "/esl/template/update"

    base_url = None
    token = None

    def __init__(self, username: str, password: str, base_url: str = None):
        """
        Args:
            username (str): User's username
            password (str): User's password
            base_url (str, optional): API base URL. Defaults to None.
        """
        self.base_url = base_url if base_url else self.BASE_URL
        self.token = self.authenticate(username, password)

    def get_headers(self, extra_headers: dict = None):
        """
        Builds and returns the headers for an API request.

        Args:
            extra_headers (_dict_): Additional headers to be included (optional)

        Returns:
            dict: A dictionary containing the headers for the request.
        """
        headers = {"Content-Type": "application/json"}

        # Add Authorization token if available
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        # Merge with extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        return headers

    def build_url(self, endpoint: str, **kwargs):
        """Returns the absolute url of the API

        Args:
            endpoint (_str_): Relative url for the endpoint

        Returns:
            str: Absolute url
        """

        return f"{self.base_url}{endpoint}"

    def request(
        self,
        method: str,
        url: str,
        headers: dict,
        data: dict = None,
        params: dict = None,
        timeout: int = 60,
        debug: bool = False,
        **kwargs,
    ):
        req_method = getattr(requests, method)
        url = self.build_url(url)

        try:
            response = req_method(
                url,
                json=data,
                params=params,
                headers=headers,
                timeout=timeout,
                verify=True,
                stream=False,
            )

            response = self.validate_response(response=response)
        except requests.exceptions.Timeout:
            raise TimeoutError
        except requests.RequestException as e:
            raise APIError(e)
        except Exception as e:
            raise
        return response

    def validate_response(self, response: requests.Response):
        """Validates HTTP response and raises errors if any."""
        if not response.ok:
            raise APIError(f"Error: {response.status_code} - {response.text}")

    def parse_response(
        self, response: requests.Response, err_msg: str
    ) -> tuple[dict, int, str]:
        """
        Returns a 3-tuple containing the json-encoded content of response
        (index 0), code (index 1) and msg (index 2)

        Args:
            response (requests.Response): Response received from the API.
            err_msg (str): The message that must be shown in case of an error.
                This can be of the form: "Error: {code} and Message {msg}",
                `{code}` and `{msg}` will be interpolated using the format
                function and only `code` and `msg` are valid variables.
                Example: "Login failed: Code: {code} - Message: {msg}"

        Raises:
            APIError: In case the `code` attribute of the response is not 200,
                      and exception is raise.

        Returns:
            tuple[dict, int, str]
        """
        response = response.json()

        msg = response.get("msg", False)
        if not msg:
            msg = response.get("message", "")

        code = response.get("code", None)
        if code != 200:
            raise APIError(err_msg.format(code=code, msg=msg))

        return response, code, msg

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        """Sends a GET request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        return self.request("get", endpoint, headers=headers, params=params)

    def post(self, endpoint: str, data: dict, headers: dict = None):
        """Sends a POST request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        return self.request("post", endpoint, headers=headers, data=data)

    def put(self, endpoint: str, data: dict, headers: dict = None):
        """Sends a PUT request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        return self.request("put", endpoint, headers=headers, data=data)

    def delete(self, endpoint: str, params: dict = None, headers: dict = None):
        """Sends a DELETE request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        return self.request(
            "delete", endpoint, headers=headers, params=params
        )

    def authenticate(self, username: str, password: str):
        """Authenticates the user and retrieves the token."""
        password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()

        data = {"username": username, "password": password_md5}

        response = self.post(self.LOGIN_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Login failed: Code: {code} - Message: {msg}"
        )

        self.token = response.get("data", {}).get("token")

        return self.token

    # Store API
    def store_add(self, number: str, name: str, address: str) -> str:
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

        response = self.post(self.STORE_ADD_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Store creation failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("storeId")

    def store_modify(
        self, id: str, name: str, address: str, active: int
    ) -> str:
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

        response = self.put(self.STORE_UPDATE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Store modification failed: Code: {code} - Message: {msg}"
        )

        return msg

    def store_close_or_open(self, id: str, active: int) -> str:
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

        response = self.get(self.STORE_ACTIVE_ENDPOINT, params)

        _, _, msg = self.parse_response(
            response,
            "Store {action} failed: Code: {code} - Message: {msg}"
        )

        return msg

    def store_get_information(
        self, active: int = 1, condition: str = None
    ) -> list[dict]:
        """
        Retrieves information about stores based on active status or condition.

        Args:
            active (int): 1 to get active stores, 0 for inactive stores
            condition (str, optional): Optional store name, number, or address
                to filter results

        Returns:
            list[dict]: API response containing store information
        """

        params = {"active": active, "condition": condition}

        response = self.get(self.STORE_LIST_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Retrieving information about stores failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", [])
    def store_get_warnings(self, store_id: str, screening: str = None) -> dict:
        """
        Retrieves warning information for a specific store.

        Args:
            store_id (str): The store's ID
            screening (str, optional): 'brush' for brush warnings, 'upgrade'
                for upgrade warnings

        Returns:
            dict: API response containing warning details
        """

        params = {"storeId": store_id, "screening": screening}

        response = self.get(self.STORE_WARNING_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Retrieving warning information failed: Code: {code} - Message: {msg}"
        )

        return response

    def store_get_logs(
        self,
        store_id: str,
        current_page: int,
        page_size: int,
        object_type: str,
        action_type: str = "",
        condition: str = "",
    ) -> dict:
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
            dict: API response containing log information

        Response parameters:
            code (int): See error code for details
            msg (str): information
            currentPage (int): Page of inquiry
            pageSize (int): Number of items are displayed on each page
            totalNum (int): Total number of items
            isMore (int): 1 Represents has next page
            totalPage (int): Total of pages
            startIndex (int): Start index
            Items (List<T>): Data collection
            operator (str): Operator
            createTime (str): Request time: yyyy-MM-dd HH-mm-ss
            actionType (str): Action type:
                1 Refresh label
                2 Uprade
                3 Add
                4 Delete
                5 Binding
                6 Appointed sent demand
                7 Warning light
            result (str): Operation result:
                1 Refresh successfully
                2 Refresh failed
                3 Error key
                4 Upgrade successfully
                5 Upgrade failed
                6 Invalid firmware package
                7 Refresh overtime
                8 Upgrade overtime
                9 Abnormal screen
                10 Gateway offline
                11 Template error or does not exist
                12 Gateway hardware issue
        """

        data = {
            "storeId": store_id,
            "currentPage": current_page,
            "pageSize": page_size,
            "objectType": object_type,
            "actionType": action_type,
            "condition": condition,
        }

        response = self.post(self.STORE_LOGS_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Retrieving operation log information failed: Code: {code} - Message: {msg}"
        )

        return response

    def template_list(
        self,
        store_id: str,
        page: int,
        size: int,
        screening: int = 0,
        inch: float = None,
        color: str = None,
        fuzzy: str = None,
    ) -> dict:
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
            dict: API response containing templates information
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

        response = self.get(self.TEMPLATE_LIST_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Template list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("rows", [])

    def template_preview_unbound(self, demo_name: str) -> str:
        """
        Previews a template that is not bound to any data.

        Args:
            demo_name (str): Template name

        Returns:
            str: API response containing the image preview in base64 format
        """
        data = {"demoName": demo_name}

        response = self.post(self.TEMPLATE_PREVIEW_UNBOUND_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Template unbound preview failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", "")

    def template_preview_bound(
        self, demo_name: str, data_id: str, store_id: str
    ) -> str:
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

        response = self.post(self.TEMPLATE_PREVIEW_BOUND_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Template bound preview failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", "")

    # Gateway: Add Gateway
    def gateway_add(self, mac: str, name: str, store_id: str) -> str:
        """
        Adds a new gateway to the store.

        Args:
            mac (str): Gateway MAC address
            name (str): Gateway name
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/gateway/add
        Request Method: POST
        Request Example:
            {
                "mac": "AC233FC03CEC",
                "name": "GW-AC233FC03CEC",
                "storeId": "1328266049345687552"
            }

        Response Parameters:
            code (int): Response code (e.g., 200 for success)
            message (str): Response message (e.g., "success")
            data (None)
        """
        data = {
            "mac": mac,
            "name": name,
            "storeId": store_id
        }

        response = self.post(self.GATEWAY_ADD_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Gateway add failed: Code: {code} - Message: {msg}"
        )

        return response.get("message", "Success")

    # Gateway: Delete Gateway
    def gateway_delete(self, gateway_id: str, store_id: str) -> str:
        """
        Deletes a gateway from the store.

        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/gateway/delete
        Request Method: GET
        Request Example:
            /esl/gateway/delete?id=1349244935877955584&storeId=1328266049345687552

        Response Parameters:
            code (int): Response code (e.g., 200 for success)
            message (str): Response message (e.g., "success")
            data (None)
        """
        params = {
            "id": gateway_id,
            "storeId": store_id
        }

        response = self.get(self.GATEWAY_DELETE_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Gateway delete failed: Code: {code} - Message: {msg}"
        )

        return response.get("message", "Success")

    # Gateway: Query Gateway List
    def gateway_list(self, store_id: str, page: int, size: int) -> list[dict]:
        """
        Retrieves the list of gateways for a store.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page

        Returns:
            list[dict]: List of gateway information

        API URL: /esl/gateway/listPage
        Request Method: GET
        Request Example:
            /esl/gateway/listPage?page=1&size=10&storeId=1326065100695539712

        Response Parameters:
            code (int): Response code (e.g., 200 for success)
            currentPage (int): Current page number
            pageSize (int): Number of items per page
            totalNum (int): Total number of items
            isMore (int): 1 if there are more pages, 0 otherwise
            totalPage (int): Total number of pages
            startIndex (int): Start index
            items (list[dict]): List of gateway information
                id (str): Gateway ID
                name (str): Gateway name
                mac (str): Gateway MAC address
                mode (int): 1 for online, 0 for offline
                hardware (str): Hardware version
                firmware (str): Firmware version
                product (str): Product model
                createTime (str): Gateway creation time
                updateTime (str): Gateway update time
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        response = self.get(self.GATEWAY_LIST_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Gateway list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response.get("items", [])

    # Gateway: Modify Gateway Information
    def gateway_modify(self, gateway_id: str, name: str) -> str:
        """
        Modifies the information of a gateway.

        Args:
            gateway_id (str): Gateway ID or MAC address
            name (str): Gateway name

        Returns:
            str: Success message from the API

        API URL: /esl/gateway/update
        Request Method: POST
        Request Example:
            {
                "id": "1339854807833251840",
                "name": "AC233FC03D511"
            }

        Response Parameters:
            code (int): Response code (e.g., 200 for success)
            message (str): Response message (e.g., "success")
            data (None)
        """
        data = {
            "id": gateway_id,
            "name": name
        }

        response = self.post(self.GATEWAY_UPDATE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Gateway modification failed: Code: {code} - Message: {msg}"
        )

        return msg
        
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

        API URL: /esl/label/add
        Request Method: POST
        """
        data = {
            "mac": mac,
            "storeId": store_id,
            "demoName": demo_name
        }

        response = self.post(self.LABEL_ADD_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Label add failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("labelId", "")

    def label_list(self, store_id: str, page: int, size: int, condition: str = None) -> dict:
        """
        Retrieves a list of labels in a store.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            condition (str, optional): Filter condition (e.g., label MAC or name)

        Returns:
            dict: Dictionary containing label information and pagination details

        API URL: /esl/label/list
        Request Method: GET
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        if condition:
            params["condition"] = condition

        response = self.get(self.LABEL_LIST_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Label list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response

    def label_delete(self, label_id: str, store_id: str) -> str:
        """
        Deletes a label from the system.

        Args:
            label_id (str): Label ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/label/delete
        Request Method: GET
        """
        params = {
            "id": label_id,
            "storeId": store_id
        }

        response = self.get(self.LABEL_DELETE_ENDPOINT, params)

        _, _, msg = self.parse_response(
            response,
            "Label delete failed: Code: {code} - Message: {msg}"
        )

        return msg

    def label_update(self, label_id: str, name: str) -> str:
        """
        Updates an existing label's information.

        Args:
            label_id (str): Label ID
            name (str): New label name

        Returns:
            str: Success message from the API

        API URL: /esl/label/update
        Request Method: POST
        """
        data = {
            "id": label_id,
            "name": name
        }

        response = self.post(self.LABEL_UPDATE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Label update failed: Code: {code} - Message: {msg}"
        )

        return msg

    def label_binding(self, label_id: str, data_id: str, store_id: str) -> str:
        """
        Binds a label to a product/data item.

        Args:
            label_id (str): Label ID
            data_id (str): Data/Product ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/label/binding
        Request Method: POST
        """
        data = {
            "labelId": label_id,
            "dataId": data_id,
            "storeId": store_id
        }

        response = self.post(self.LABEL_BINDING_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Label binding failed: Code: {code} - Message: {msg}"
        )

        return msg

    def label_refresh(self, label_ids: list, store_id: str) -> str:
        """
        Refreshes the display of one or more labels.

        Args:
            label_ids (list): List of label IDs to refresh
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/label/refresh
        Request Method: POST
        """
        data = {
            "labelIds": label_ids,
            "storeId": store_id
        }

        response = self.post(self.LABEL_REFRESH_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Label refresh failed: Code: {code} - Message: {msg}"
        )

        return msg
        
    # Data API Methods
    def data_add(self, store_id: str, product_data: dict) -> str:
        """
        Adds product data to the system.

        Args:
            store_id (str): Store ID
            product_data (dict): Dictionary containing product information

        Returns:
            str: Data ID if successful

        API URL: /esl/data/add
        Request Method: POST
        """
        data = {
            "storeId": store_id,
            **product_data
        }

        response = self.post(self.DATA_ADD_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Data add failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("dataId", "")

    def data_update(self, data_id: str, store_id: str, product_data: dict) -> str:
        """
        Updates existing product data.

        Args:
            data_id (str): Data ID
            store_id (str): Store ID
            product_data (dict): Dictionary containing updated product information

        Returns:
            str: Success message from the API

        API URL: /esl/data/update
        Request Method: PUT
        """
        data = {
            "id": data_id,
            "storeId": store_id,
            **product_data
        }

        response = self.put(self.DATA_UPDATE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Data update failed: Code: {code} - Message: {msg}"
        )

        return msg

    def data_delete(self, data_id: str, store_id: str) -> str:
        """
        Deletes product data from the system.

        Args:
            data_id (str): Data ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/data/delete
        Request Method: GET
        """
        params = {
            "id": data_id,
            "storeId": store_id
        }

        response = self.get(self.DATA_DELETE_ENDPOINT, params)

        _, _, msg = self.parse_response(
            response,
            "Data delete failed: Code: {code} - Message: {msg}"
        )

        return msg

    def data_list(self, store_id: str, page: int, size: int, condition: str = None) -> dict:
        """
        Retrieves a list of product data items.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page
            condition (str, optional): Filter condition (e.g., product name)

        Returns:
            dict: Dictionary containing product data information and pagination details

        API URL: /esl/data/list
        Request Method: GET
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        if condition:
            params["condition"] = condition

        response = self.get(self.DATA_LIST_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Data list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response
        
    def data_binding_list(self, store_id: str, page: int, size: int) -> dict:
        """
        Gets a list of data items bound to labels.

        Args:
            store_id (str): Store ID
            page (int): Page number for pagination
            size (int): Number of items per page

        Returns:
            dict: Dictionary containing bound data information and pagination details

        API URL: /esl/data/bindingList
        Request Method: GET
        """
        params = {
            "storeId": store_id,
            "page": page,
            "size": size
        }

        response = self.get(self.DATA_BINDING_LIST_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Data binding list retrieval failed: Code: {code} - Message: {msg}"
        )

        return response
        
    # Template additional methods
    def template_add(self, store_id: str, template_name: str, content: str) -> str:
        """
        Adds a new template to the system.

        Args:
            store_id (str): Store ID
            template_name (str): Template name
            content (str): Template content

        Returns:
            str: Template ID if successful

        API URL: /esl/template/add
        Request Method: POST
        """
        data = {
            "storeId": store_id,
            "templateName": template_name,
            "content": content
        }

        response = self.post(self.TEMPLATE_ADD_ENDPOINT, data)

        response, _, _ = self.parse_response(
            response,
            "Template add failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {}).get("templateId", "")

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

        API URL: /esl/template/update
        Request Method: PUT
        """
        data = {
            "id": template_id,
            "storeId": store_id,
            "templateName": template_name,
            "content": content
        }

        response = self.put(self.TEMPLATE_UPDATE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Template update failed: Code: {code} - Message: {msg}"
        )

        return msg

    def template_delete(self, template_id: str, store_id: str) -> str:
        """
        Deletes a template from the system.

        Args:
            template_id (str): Template ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/template/delete
        Request Method: GET
        """
        params = {
            "id": template_id,
            "storeId": store_id
        }

        response = self.get(self.TEMPLATE_DELETE_ENDPOINT, params)

        _, _, msg = self.parse_response(
            response,
            "Template delete failed: Code: {code} - Message: {msg}"
        )

        return msg
        
    # Gateway additional methods
    def gateway_restart(self, gateway_id: str, store_id: str) -> str:
        """
        Restarts a specific gateway.

        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/gateway/restart
        Request Method: GET
        """
        params = {
            "id": gateway_id,
            "storeId": store_id
        }

        response = self.get(self.GATEWAY_RESTART_ENDPOINT, params)

        _, _, msg = self.parse_response(
            response,
            "Gateway restart failed: Code: {code} - Message: {msg}"
        )

        return msg

    def gateway_upgrade(self, gateway_id: str, store_id: str, firmware_version: str) -> str:
        """
        Upgrades gateway firmware.

        Args:
            gateway_id (str): Gateway ID
            store_id (str): Store ID
            firmware_version (str): Firmware version to upgrade to

        Returns:
            str: Success message from the API

        API URL: /esl/gateway/upgrade
        Request Method: POST
        """
        data = {
            "gatewayId": gateway_id,
            "storeId": store_id,
            "firmwareVersion": firmware_version
        }

        response = self.post(self.GATEWAY_UPGRADE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Gateway upgrade failed: Code: {code} - Message: {msg}"
        )

        return msg
        
    # Label additional methods
    def label_unbinding(self, label_id: str, store_id: str) -> str:
        """
        Unbinds a label from its product/data association.

        Args:
            label_id (str): Label ID
            store_id (str): Store ID

        Returns:
            str: Success message from the API

        API URL: /esl/label/unbinding
        Request Method: GET
        """
        params = {
            "labelId": label_id,
            "storeId": store_id
        }

        response = self.get(self.LABEL_UNBINDING_ENDPOINT, params)

        _, _, msg = self.parse_response(
            response,
            "Label unbinding failed: Code: {code} - Message: {msg}"
        )

        return msg

    def label_upgrade(self, label_ids: list, store_id: str, firmware_version: str) -> str:
        """
        Upgrades label firmware.

        Args:
            label_ids (list): List of label IDs to upgrade
            store_id (str): Store ID
            firmware_version (str): Firmware version to upgrade to

        Returns:
            str: Success message from the API

        API URL: /esl/label/upgrade
        Request Method: POST
        """
        data = {
            "labelIds": label_ids,
            "storeId": store_id,
            "firmwareVersion": firmware_version
        }

        response = self.post(self.LABEL_UPGRADE_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Label upgrade failed: Code: {code} - Message: {msg}"
        )

        return msg

    def label_find_by_mac(self, mac: str, store_id: str) -> dict:
        """
        Finds a label by its MAC address.

        Args:
            mac (str): Label MAC address
            store_id (str): Store ID

        Returns:
            dict: Label information

        API URL: /esl/label/findByMac
        Request Method: GET
        """
        params = {
            "mac": mac,
            "storeId": store_id
        }

        response = self.get(self.LABEL_FIND_BY_MAC_ENDPOINT, params)

        response, _, _ = self.parse_response(
            response,
            "Label find by MAC failed: Code: {code} - Message: {msg}"
        )

        return response.get("data", {})

    def label_flash(self, label_id: str, store_id: str, flash_mode: int) -> str:
        """
        Flashes the label LED for visual identification.

        Args:
            label_id (str): Label ID
            store_id (str): Store ID
            flash_mode (int): LED flash mode (e.g., 1 for flashing, 0 for static)

        Returns:
            str: Success message from the API

        API URL: /esl/label/flash
        Request Method: POST
        """
        data = {
            "labelId": label_id,
            "storeId": store_id,
            "flashMode": flash_mode
        }

        response = self.post(self.LABEL_FLASH_ENDPOINT, data)

        _, _, msg = self.parse_response(
            response,
            "Label flash failed: Code: {code} - Message: {msg}"
        )

        return msg
