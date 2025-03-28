"""
Base classes for the Minew API client.
"""
import hashlib
import requests
from typing import Dict, Optional, Tuple, Any, List, Union

from .exceptions import APIError


class BaseClient:
    """
    Base client for Minew API containing core functionality.
    """
    BASE_URL = "https://cloud.minewtag.com/apis/"
    LOGIN_ENDPOINT = "/action/login"

    def __init__(self, username: str, password: str, base_url: Optional[str] = None):
        """
        Initialize the client with credentials.

        Args:
            username (str): User's username
            password (str): User's password
            base_url (str, optional): API base URL. Defaults to None.
        """
        self.base_url = base_url if base_url else self.BASE_URL
        self.token = None
        self.authenticate(username, password)

    def get_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Build and return headers for an API request.

        Args:
            extra_headers (Dict[str, str], optional): Additional headers to include

        Returns:
            Dict[str, str]: Headers for the request
        """
        headers = {"Content-Type": "application/json"}

        # Add Authorization token if available
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        # Merge with extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        return headers

    def build_url(self, endpoint: str) -> str:
        """
        Build the full URL for an API endpoint.

        Args:
            endpoint (str): Relative URL for the endpoint

        Returns:
            str: Absolute URL
        """
        return f"{self.base_url}{endpoint}"

    def request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 60,
        debug: bool = False,
        **kwargs
    ) -> requests.Response:
        """
        Send an HTTP request to the API.

        Args:
            method (str): HTTP method (get, post, put, delete)
            url (str): Endpoint URL
            headers (Dict[str, str]): Request headers
            data (Dict[str, Any], optional): Request body data
            params (Dict[str, Any], optional): Query parameters
            timeout (int, optional): Request timeout in seconds
            debug (bool, optional): Enable debug mode
            **kwargs: Additional keyword arguments

        Returns:
            requests.Response: HTTP response

        Raises:
            APIError: If the API returns an error
            TimeoutError: If the request times out
        """
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
            raise TimeoutError("Request timed out")
        except requests.RequestException as e:
            raise APIError(str(e))
        
        return response

    def validate_response(self, response: requests.Response) -> requests.Response:
        """
        Validate HTTP response and raise errors if needed.

        Args:
            response (requests.Response): Response to validate

        Returns:
            requests.Response: Validated response

        Raises:
            APIError: If the response indicates an error
        """
        if not response.ok:
            raise APIError(f"Error: {response.status_code} - {response.text}")
        
        return response

    def parse_response(
        self, response: requests.Response, err_msg: str
    ) -> Tuple[Dict[str, Any], int, str]:
        """
        Parse API response and handle errors.

        Args:
            response (requests.Response): Response from the API
            err_msg (str): Error message template with {code} and {msg} placeholders

        Returns:
            Tuple[Dict[str, Any], int, str]: Response data, code, and message

        Raises:
            APIError: If the response code is not 200
        """
        response_data = response.json()

        msg = response_data.get("msg", False)
        if not msg:
            msg = response_data.get("message", "")

        code = response_data.get("code", None)
        if code != 200:
            raise APIError(err_msg.format(code=code, msg=msg))

        return response_data, code, str(msg)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send a GET request to the API.

        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers

        Returns:
            requests.Response: API response
        """
        headers = self.get_headers(extra_headers=headers)
        return self.request("get", endpoint, headers=headers, params=params)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send a POST request to the API.

        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any]): Request body
            headers (Dict[str, str], optional): Additional headers

        Returns:
            requests.Response: API response
        """
        headers = self.get_headers(extra_headers=headers)
        return self.request("post", endpoint, headers=headers, data=data)

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send a PUT request to the API.

        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any]): Request body
            headers (Dict[str, str], optional): Additional headers

        Returns:
            requests.Response: API response
        """
        headers = self.get_headers(extra_headers=headers)
        return self.request("put", endpoint, headers=headers, data=data)

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send a DELETE request to the API.

        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers

        Returns:
            requests.Response: API response
        """
        headers = self.get_headers(extra_headers=headers)
        return self.request("delete", endpoint, headers=headers, params=params)

    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticate with the API and get a token.

        Args:
            username (str): User's username
            password (str): User's password

        Returns:
            str: Authentication token

        Raises:
            APIError: If authentication fails
        """
        password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()

        data = {"username": username, "password": password_md5}

        response = self.post(self.LOGIN_ENDPOINT, data)

        response_data, _, _ = self.parse_response(
            response,
            "Login failed: Code: {code} - Message: {msg}"
        )

        token = response_data.get("data", {}).get("token")
        if token is None:
            token = ""
            
        self.token = token
        return token


class BaseResource:
    """
    Base class for API resources.
    """
    def __init__(self, client: BaseClient):
        """
        Initialize with a client instance.

        Args:
            client (BaseClient): API client instance
        """
        self.client = client


