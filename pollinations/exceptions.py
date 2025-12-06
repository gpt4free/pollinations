"""Custom exceptions for Pollinations API."""


class PollinationsError(Exception):
    """Base exception for all Pollinations errors."""
    pass


class APIError(PollinationsError):
    """Raised when the API returns an error."""
    
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)


class ModelNotFoundError(PollinationsError):
    """Raised when a requested model is not found."""
    pass
