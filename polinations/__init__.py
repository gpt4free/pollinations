"""
Polinations - Python wrapper for Polinations AI

A simple and easy-to-use Python library for accessing Polinations AI's free text and image generation APIs.
"""

from .client import Polinations
from .exceptions import PolinationsError, APIError, ModelNotFoundError

__version__ = "0.1.0"
__all__ = ["Polinations", "PolinationsError", "APIError", "ModelNotFoundError"]
