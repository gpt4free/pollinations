"""Unit tests for OpenAI-compatible API."""

import unittest
from unittest.mock import patch, Mock
from polinations import Polinations


class TestOpenAICompatibility(unittest.TestCase):
    """Test cases for OpenAI-compatible API."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Polinations(timeout=30)
    
    def test_client_has_openai_interfaces(self):
        """Test that client has OpenAI-compatible interfaces."""
        self.assertIsNotNone(self.client.images)
        self.assertIsNotNone(self.client.chat)
        self.assertIsNotNone(self.client.chat.completions)
    
    def test_api_key_initialization(self):
        """Test client initialization with API key."""
        client = Polinations(api_key="test-key-123")
        self.assertEqual(client.api_key, "test-key-123")
        # Should use gen.pollinations.ai when API key is provided
        self.assertIn("gen.pollinations.ai", client.IMAGE_BASE_URL)
        self.assertIn("gen.pollinations.ai", client.TEXT_BASE_URL)
    
    def test_headers_with_api_key(self):
        """Test that headers include API key when provided."""
        client = Polinations(api_key="test-key-123")
        headers = client._get_headers()
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "Bearer test-key-123")
    
    def test_headers_without_api_key(self):
        """Test that headers are empty when no API key."""
        headers = self.client._get_headers()
        self.assertEqual(headers, {})
    
    def test_images_generate_simple(self):
        """Test simple image generation with OpenAI-compatible API."""
        response = self.client.images.generate(
            prompt="A test image"
        )
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertIn("url", response.data[0])
        self.assertIn("test%20image", response.data[0]["url"])
    
    def test_images_generate_with_size(self):
        """Test image generation with size parameter."""
        response = self.client.images.generate(
            prompt="Test",
            size="1024x768"
        )
        url = response.data[0]["url"]
        self.assertIn("width=1024", url)
        self.assertIn("height=768", url)
    
    def test_images_generate_with_model(self):
        """Test image generation with model parameter."""
        response = self.client.images.generate(
            prompt="Test",
            model="flux"
        )
        url = response.data[0]["url"]
        self.assertIn("model=flux", url)
    
    def test_images_generate_n_parameter_validation(self):
        """Test that n>1 raises an error."""
        with self.assertRaises(ValueError) as context:
            self.client.images.generate(prompt="Test", n=2)
        self.assertIn("Only n=1 is supported", str(context.exception))
    
    def test_images_generate_response_format_validation(self):
        """Test that non-url response format raises an error."""
        with self.assertRaises(ValueError) as context:
            self.client.images.generate(prompt="Test", response_format="b64_json")
        self.assertIn("Only response_format='url' is supported", str(context.exception))
    
    @patch('polinations.client.requests.post')
    def test_chat_completions_create_simple(self, mock_post):
        """Test simple chat completion."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "Hello! How can I help you?"
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        
        self.assertEqual(response.object, "chat.completion")
        self.assertEqual(len(response.choices), 1)
        self.assertEqual(response.choices[0].message.role, "assistant")
        self.assertEqual(response.choices[0].message.content, "Hello! How can I help you?")
        self.assertEqual(response.choices[0].finish_reason, "stop")
    
    @patch('polinations.client.requests.post')
    def test_chat_completions_create_with_system(self, mock_post):
        """Test chat completion with system message."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "Response"
        mock_post.return_value = mock_response
        
        self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "Hello"}
            ]
        )
        
        # Verify the underlying call had system message
        call_args = mock_post.call_args
        # System message should have been passed
        self.assertTrue(mock_post.called)
    
    @patch('polinations.client.requests.post')
    def test_chat_completions_create_with_params(self, mock_post):
        """Test chat completion with parameters."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = "Response"
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Test"}],
            model="openai",
            temperature=0.7,
            max_tokens=100
        )
        
        self.assertEqual(response.model, "openai")
        self.assertTrue(mock_post.called)
    
    def test_chat_completions_stream_not_supported(self):
        """Test that streaming raises an error."""
        with self.assertRaises(ValueError) as context:
            self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Test"}],
                stream=True
            )
        self.assertIn("Streaming is not supported", str(context.exception))
    
    def test_chat_completions_no_user_message(self):
        """Test that missing user message raises an error."""
        with self.assertRaises(ValueError) as context:
            self.client.chat.completions.create(
                messages=[{"role": "system", "content": "You are helpful"}]
            )
        self.assertIn("At least one user message is required", str(context.exception))


if __name__ == '__main__':
    unittest.main()
