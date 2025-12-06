"""
Pollinations - Python wrapper for Pollinations AI

A simple and easy-to-use Python library for accessing Pollinations AI's free text and image generation APIs.
"""

from .client import Pollinations
from .exceptions import PollinationsError, APIError, ModelNotFoundError

__version__ = "0.1.0"
__all__ = ["Pollinations", "PollinationsError", "APIError", "ModelNotFoundError"]
