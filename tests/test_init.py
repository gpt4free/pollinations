"""Test package initialization."""

import unittest
from pollinations import Pollinations, APIError, ModelNotFoundError, __version__


class TestPackage(unittest.TestCase):
    """Test package-level functionality."""
    
    def test_imports(self):
        """Test that main classes can be imported."""
        self.assertIsNotNone(Pollinations)
        self.assertIsNotNone(APIError)
        self.assertIsNotNone(ModelNotFoundError)
    
    def test_version(self):
        """Test that version is defined."""
        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)
        self.assertTrue(len(__version__) > 0)


if __name__ == '__main__':
    unittest.main()
