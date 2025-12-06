"""Custom exceptions for Polinations API."""


class PolinationsError(Exception):
    """Base exception for all Polinations errors."""
    pass


class APIError(PolinationsError):
    """Raised when the API returns an error."""
    
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)


class ModelNotFoundError(PolinationsError):
    """Raised when a requested model is not found."""
    pass
