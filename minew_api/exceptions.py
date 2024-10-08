
class APIError(Exception):
    """Exception raised for API errors."""
    def __init__(self, message):
        super().__init__(message)


class AuthorizationError(APIError):
    pass


class ActionDeniedError(APIError):
    pass


class CriticalAPIError(APIError):
    pass


class ApiRateLimitError(APIError):
    pass


class TimeoutError(APIError):
    pass


class DoesNotExistError(APIError):
    pass


class ValidationError(APIError):
    pass
