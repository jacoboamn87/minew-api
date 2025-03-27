"""
Minew Cloud Platform API Client Library.

This library provides a Python interface to the Minew Cloud Platform API
for Electronic Shelf Label (ESL) systems.
"""

__version__ = "1.1.0"

from .client import MinewAPIClient
from .exceptions import (
    APIError,
    AuthorizationError,
    ActionDeniedError,
    CriticalAPIError,
    ApiRateLimitError,
    TimeoutError,
    DoesNotExistError,
    ValidationError,
)

__all__ = [
    "MinewAPIClient",
    "APIError",
    "AuthorizationError",
    "ActionDeniedError",
    "CriticalAPIError",
    "ApiRateLimitError",
    "TimeoutError",
    "DoesNotExistError",
    "ValidationError",
]
