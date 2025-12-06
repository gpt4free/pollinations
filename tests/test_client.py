"""Unit tests for Polinations client."""

import unittest
from unittest.mock import patch, Mock
from polinations import Polinations, APIError, ModelNotFoundError


class TestPolinations(unittest.TestCase):
    """Test cases for Polinations client."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Polinations(timeout=30)
    
    def test_client_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.timeout, 30)
        self.assertIsNone(self.client._image_models_cache)
        self.assertIsNone(self.client._text_models_cache)
    
    def test_generate_image_url_simple(self):
        """Test simple image URL generation."""
        url = self.client.generate_image("test prompt")
        self.assertIn("https://image.pollinations.ai/prompt/", url)
        self.assertIn("test%20prompt", url)
    
    def test_generate_image_url_with_params(self):
        """Test image URL generation with parameters."""
        url = self.client.generate_image(
            "test",
            model="flux",
            width=1024,
            height=768,
            seed=42,
            nologo=True,
            private=True,
            enhance=True
        )
        self.assertIn("model=flux", url)
        self.assertIn("width=1024", url)
        self.assertIn("height=768", url)
        self.assertIn("seed=42", url)
        self.assertIn("nologo=true", url)
        self.assertIn("private=true", url)
        self.assertIn("enhance=true", url)
    
    def test_generate_image_url_encoding(self):
        """Test URL encoding in image generation."""
        url = self.client.generate_image("hello world! #test")
        self.assertIn("hello%20world", url)
        self.assertIn("%23test", url)
    
    @patch('polinations.client.requests.get')
    def test_get_image_models_success(self, mock_get):
        """Test successful retrieval of image models."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = ["flux", "stable-diffusion", "dall-e"]
        mock_get.return_value = mock_response
        
        models = self.client.get_image_models()
        
        self.assertEqual(len(models), 3)
        self.assertIn("flux", models)
        mock_get.assert_called_once()
    
    @patch('polinations.client.requests.get')
    def test_get_image_models_caching(self, mock_get):
        """Test model caching."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = ["flux", "stable-diffusion"]
        mock_get.return_value = mock_response
        
        # First call
        models1 = self.client.get_image_models()
        # Second call should use cache
        models2 = self.client.get_image_models()
        
        self.assertEqual(models1, models2)
        mock_get.assert_called_once()  # Should only call API once
    
    @patch('polinations.client.requests.get')
    def test_get_image_models_force_refresh(self, mock_get):
        """Test force refresh of model cache."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = ["flux"]
        mock_get.return_value = mock_response
        
        # First call
        self.client.get_image_models()
        # Force refresh
        self.client.get_image_models(force_refresh=True)
        
        self.assertEqual(mock_get.call_count, 2)
    
    @patch('polinations.client.requests.get')
    def test_get_image_models_error(self, mock_get):
        """Test error handling when fetching models."""
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        with self.assertRaises(APIError) as context:
            self.client.get_image_models()
        
        self.assertIn("Failed to fetch image models", str(context.exception))
    
    @patch('polinations.client.requests.post')
    def test_generate_text_success(self, mock_post):
        """Test successful text generation."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "This is a test response"
        mock_post.return_value = mock_response
        
        response = self.client.generate_text("Hello")
        
        self.assertEqual(response, "This is a test response")
        mock_post.assert_called_once()
        
        # Check the request payload
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn('messages', payload)
        self.assertEqual(payload['messages'][0]['role'], 'user')
        self.assertEqual(payload['messages'][0]['content'], 'Hello')
    
    @patch('polinations.client.requests.post')
    def test_generate_text_with_params(self, mock_post):
        """Test text generation with parameters."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "Response"
        mock_post.return_value = mock_response
        
        self.client.generate_text(
            "Test",
            model="openai",
            system="You are helpful",
            temperature=0.7,
            max_tokens=100,
            seed=42,
            jsonMode=True
        )
        
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['model'], 'openai')
        self.assertEqual(payload['temperature'], 0.7)
        self.assertEqual(payload['max_tokens'], 100)
        self.assertEqual(payload['seed'], 42)
        self.assertTrue(payload['jsonMode'])
        # System message should be first
        self.assertEqual(payload['messages'][0]['role'], 'system')
        self.assertEqual(payload['messages'][0]['content'], 'You are helpful')
    
    @patch('polinations.client.requests.post')
    def test_generate_text_with_zero_max_tokens(self, mock_post):
        """Test that max_tokens=0 is properly handled."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "Response"
        mock_post.return_value = mock_response
        
        self.client.generate_text("Test", max_tokens=0)
        
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        # max_tokens should be present even when set to 0
        self.assertIn('max_tokens', payload)
        self.assertEqual(payload['max_tokens'], 0)
    
    @patch('polinations.client.requests.post')
    def test_generate_text_error(self, mock_post):
        """Test error handling in text generation."""
        import requests
        mock_post.side_effect = requests.RequestException("API error")
        
        with self.assertRaises(APIError) as context:
            self.client.generate_text("Test")
        
        self.assertIn("Failed to generate text", str(context.exception))
    
    @patch('polinations.client.requests.get')
    def test_download_image_success(self, mock_get):
        """Test successful image download."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response
        
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
            output_path = f.name
        
        try:
            result = self.client.download_image("test", output_path)
            
            self.assertEqual(result, output_path)
            self.assertTrue(os.path.exists(output_path))
            
            with open(output_path, 'rb') as f:
                content = f.read()
            self.assertEqual(content, b"fake image data")
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_api_error_with_status_code(self):
        """Test APIError with status code."""
        error = APIError("Test error", 404)
        self.assertEqual(error.status_code, 404)
        self.assertEqual(str(error), "Test error")
    
    def test_model_not_found_error(self):
        """Test ModelNotFoundError."""
        error = ModelNotFoundError("Model not found")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Model not found")


if __name__ == '__main__':
    unittest.main()
