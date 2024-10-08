import hashlib
import requests

from .exceptions import (
    APIError
)


class MinewAPIClient(object):
    """
    Main client class to interact with the Minew API.
    Handles authentication, token management, and request dispatch.
    """

    BASE_URL = "https://cloud.minewtag.com/apis/"
    LOGIN_ENDPOINT = "/action/login"
    base_url = None
    token = None

    def __init__(self, username:str, password:str, base_url:str=None):
        """
        Args:
            username (str): User's username
            password (str): User's password
            base_url (str, optional): API base URL. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.base_url = base_url if base_url else self.BASE_URL
        self.authenticate(username, password)

    def get_headers(self, extra_headers:dict=None):
        """
        Builds and returns the headers for an API request.

        :param extra_headers: Any additional headers to include (optional).
        :return: A dictionary containing the headers for the request.
        """
        headers = {
            "Content-Type": "application/json"
        }

        # Add Authorization token if available
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        # Merge with extra headers if provided
        if extra_headers:
            headers.update(extra_headers)

        return headers

    def build_url(self, endpoint:str, **kwargs):
        """Returns the absolute url of the API

        Args:
            endpoint (_str_): Relative url for the endpoint

        Returns:
            str: Absolute url
        """

        return f"{self.base_url}{endpoint}"

    def request(
        self,
        method:str,
        url:str,
        headers:dict,
        data:dict=None,
        params:dict=None,
        timeout:int=60,
        debug:bool=False,
        **kwargs
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

            self.validate_response(response=response)

            return response
        except requests.exceptions.Timeout:
            raise TimeoutError
        except requests.RequestException as e:
            raise APIError(e)
        except Exception as e:
            raise

    # def parse_response(self, response, debug=False):
    #     data = response.json()

    #     if debug:
    #         logging.debug("REQUEST: %s" % response.request.url)
    #         logging.debug("REQUEST_HEADERS: %s" % response.request.headers)
    #         logging.debug("REQUEST_CONTENT: %s" % response.request.body)

    #         logging.debug("RESPONSE: %s" % response.content)
    #         logging.debug("RESP_HEADERS: %s" % response.headers)
    #         logging.debug("RESP_CODE: %s" % response.status_code)

    #     return data

    def validate_response(self, response:requests.Response):
        """Validates response and raises errors if any."""
        if not response.ok:
            raise APIError(
                f"Error: {response.status_code} - {response.text}"
            )

    def get(self, endpoint:str, params:dict=None, headers:dict={}):
        """Sends a GET request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        response = self.request(
            "get", endpoint, headers=headers, params=params
        )
        return response.json()

    def post(self, endpoint:str, data:dict, headers:dict={}):
        """Sends a POST request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        response = self.request(
            "post", endpoint, headers=headers, data=data
        )
        return response.json()

    def put(self, endpoint:str, data:dict, headers:dict={}):
        """Sends a PUT request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        response = self.request(
            "put", endpoint, headers=headers, data=data
        )
        return response.json()

    def delete(self, endpoint:str, params:dict=None, headers:dict={}):
        """Sends a DELETE request to the given endpoint."""
        headers = self.get_headers(extra_headers=headers)
        response = self.request(
            "delete", endpoint, headers=headers, params=params
        )
        return response.json()

    def authenticate(self, username:str, password:str):
        """Authenticates the user and retrieves the token.
        """
        password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()

        data = {
            "username": username,
            "password": password_md5
        }

        response = self.post(self.LOGIN_ENDPOINT, data)

        code = response.get("code", None)

        msg = response.get("msg", False)
        if not msg:
            msg = response.get("message", "")

        if code == 200:
            self.token = response.get("data", {}).get("token")
        else:
            raise APIError(f"Login failed: Code: {code} - Message: {msg}")
