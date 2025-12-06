"""Main client for Pollinations AI API."""

import urllib.parse
from typing import Optional, List, Dict, Any, Iterator
import requests
import json

from .exceptions import APIError, ModelNotFoundError
from .openai_compat import Images, Chat, ChatCompletionChunk, ChatCompletionChunkDelta


class Pollinations:
    """
    Client for interacting with Pollinations AI APIs.
    
    Pollinations provides free APIs for text generation (chat) and image generation.
    Supports both native API and OpenAI-compatible interfaces.
    
    Example (Native API):
        >>> client = Pollinations()
        >>> # Generate text
        >>> response = client.generate_text("Hello, how are you?")
        >>> print(response)
        >>> 
        >>> # Generate image
        >>> image_url = client.generate_image("A beautiful sunset over mountains")
        >>> print(image_url)
    
    Example (OpenAI-compatible API):
        >>> client = Pollinations(api_key="your-api-key")
        >>> # Chat completion
        >>> response = client.chat.completions.create(
        ...     model="openai",
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
        >>> print(response.choices[0].message.content)
        >>> 
        >>> # Image generation
        >>> response = client.images.generate(
        ...     prompt="A sunset",
        ...     size="1024x768"
        ... )
        >>> print(response.data[0]["url"])
    """
    
    IMAGE_BASE_URL = "https://image.pollinations.ai"
    TEXT_BASE_URL = "https://text.pollinations.ai"
    
    # Alternative API endpoints that support API keys
    GEN_IMAGE_URL = "https://gen.pollinations.ai/image"
    GEN_TEXT_URL = "https://gen.pollinations.ai/text"
    
    def __init__(self, timeout: int = 30, api_key: Optional[str] = None):
        """
        Initialize the Pollinations client.
        
        Args:
            timeout: Request timeout in seconds (default: 30)
            api_key: Optional API key for gen.pollinations.ai
                    If provided, uses authenticated endpoints
        """
        self.timeout = timeout
        self.api_key = api_key
        self._image_models_cache = None
        self._text_models_cache = None
        
        # Initialize OpenAI-compatible interfaces
        self.images = Images(self)
        self.chat = Chat(self)
        
        # Update base URLs if API key is provided
        if self.api_key:
            # Use gen.pollinations.ai when API key is provided
            self.IMAGE_BASE_URL = self.GEN_IMAGE_URL
            self.TEXT_BASE_URL = self.GEN_TEXT_URL
    
    def _get_status_code(self, exception):
        """Extract status code from requests exception if available."""
        return getattr(exception.response, 'status_code', None) if hasattr(exception, 'response') else None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API key if available."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def get_image_models(self, force_refresh: bool = False) -> List[str]:
        """
        Get list of available image generation models.
        
        Args:
            force_refresh: If True, fetch fresh data from API instead of using cache
            
        Returns:
            List of model names
            
        Raises:
            APIError: If the API request fails
        """
        if self._image_models_cache is not None and not force_refresh:
            return self._image_models_cache
        
        try:
            url = f"{self.IMAGE_BASE_URL}/models"
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            models = response.json()
            self._image_models_cache = models
            return models
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch image models: {str(e)}", self._get_status_code(e))
    
    def get_text_models(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get list of available text generation models.
        
        Args:
            force_refresh: If True, fetch fresh data from API instead of using cache
            
        Returns:
            List of model information dictionaries
            
        Raises:
            APIError: If the API request fails
        """
        if self._text_models_cache is not None and not force_refresh:
            return self._text_models_cache
        
        try:
            url = f"{self.TEXT_BASE_URL}/models"
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            models = response.json()
            self._text_models_cache = models
            return models
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch text models: {str(e)}", self._get_status_code(e))
    
    def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        validate_model: bool = False
    ) -> str:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image to generate
            model: Model name to use (optional, uses default if not specified)
            width: Image width in pixels (optional)
            height: Image height in pixels (optional)
            seed: Random seed for reproducibility (optional)
            nologo: If True, removes Pollinations logo from image (optional)
            private: If True, image won't be published to feed (optional)
            enhance: If True, automatically enhances the prompt (optional)
            validate_model: If True, validates model exists before generating (optional)
            
        Returns:
            URL of the generated image
            
        Raises:
            ModelNotFoundError: If specified model doesn't exist and validate_model is True
            APIError: If the API request fails during model validation
        """
        if model and validate_model:
            available_models = self.get_image_models()
            if model not in available_models:
                raise ModelNotFoundError(f"Model '{model}' not found. Available models: {', '.join(available_models)}")
        
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"{self.IMAGE_BASE_URL}/prompt/{encoded_prompt}"
        
        params = []
        if model:
            params.append(f"model={model}")
        if width:
            params.append(f"width={width}")
        if height:
            params.append(f"height={height}")
        if seed is not None:
            params.append(f"seed={seed}")
        if nologo:
            params.append("nologo=true")
        if private:
            params.append("private=true")
        if enhance:
            params.append("enhance=true")
        
        if params:
            url += "?" + "&".join(params)
        
        return url
    
    def download_image(
        self,
        prompt: str,
        output_path: str,
        model: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False
    ) -> str:
        """
        Generate and download an image to a local file.
        
        Args:
            prompt: Text description of the image to generate
            output_path: Local path where the image will be saved
            model: Model name to use (optional)
            width: Image width in pixels (optional)
            height: Image height in pixels (optional)
            seed: Random seed for reproducibility (optional)
            nologo: If True, removes Pollinations logo from image (optional)
            private: If True, image won't be published to feed (optional)
            enhance: If True, automatically enhances the prompt (optional)
            
        Returns:
            Path to the saved image file
            
        Raises:
            ModelNotFoundError: If specified model doesn't exist
            APIError: If the API request fails or download fails
        """
        url = self.generate_image(
            prompt=prompt,
            model=model,
            width=width,
            height=height,
            seed=seed,
            nologo=nologo,
            private=private,
            enhance=enhance
        )
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
        except requests.RequestException as e:
            raise APIError(f"Failed to download image: {str(e)}", self._get_status_code(e))
        except IOError as e:
            raise APIError(f"Failed to save image to {output_path}: {str(e)}")
    
    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
        jsonMode: bool = False
    ) -> str:
        """
        Generate text using a language model.
        
        Args:
            prompt: Input text prompt
            model: Model name to use (optional, uses default if not specified)
            system: System message to set context (optional)
            temperature: Sampling temperature 0-1 (optional, higher = more creative)
            max_tokens: Maximum tokens to generate (optional)
            seed: Random seed for reproducibility (optional)
            jsonMode: If True, output will be formatted as JSON (optional)
            
        Returns:
            Generated text response
            
        Raises:
            APIError: If the API request fails
        """
        url = f"{self.TEXT_BASE_URL}"
        
        params = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system:
            params["messages"].insert(0, {"role": "system", "content": system})
        if model:
            params["model"] = model
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if seed is not None:
            params["seed"] = seed
        if jsonMode:
            params["jsonMode"] = True
        
        try:
            response = requests.post(url, json=params, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise APIError(f"Failed to generate text: {str(e)}", self._get_status_code(e))
    
    def generate_text_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
        jsonMode: bool = False
    ) -> Iterator[ChatCompletionChunk]:
        """
        Generate text using a language model with streaming.
        
        Args:
            prompt: Input text prompt
            model: Model name to use (optional, uses default if not specified)
            system: System message to set context (optional)
            temperature: Sampling temperature 0-1 (optional, higher = more creative)
            max_tokens: Maximum tokens to generate (optional)
            seed: Random seed for reproducibility (optional)
            jsonMode: If True, output will be formatted as JSON (optional)
            
        Yields:
            ChatCompletionChunk objects with delta content
            
        Raises:
            APIError: If the API request fails
        """
        url = f"{self.TEXT_BASE_URL}"
        
        params = {
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        
        if system:
            params["messages"].insert(0, {"role": "system", "content": system})
        if model:
            params["model"] = model
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if seed is not None:
            params["seed"] = seed
        if jsonMode:
            params["jsonMode"] = True
        
        try:
            response = requests.post(
                url, 
                json=params, 
                headers=self._get_headers(), 
                timeout=self.timeout,
                stream=True
            )
            response.raise_for_status()
            
            # Parse Server-Sent Events (SSE) stream
            chunk_id = None
            first_chunk = True
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                try:
                    line_str = line.decode('utf-8')
                except UnicodeDecodeError as e:
                    # Log or skip invalid UTF-8 data
                    continue
                
                # SSE format: "data: {json}"
                if line_str.startswith('data: '):
                    json_str = line_str[6:]  # Remove "data: " prefix
                    
                    try:
                        data = json.loads(json_str)
                    except json.JSONDecodeError:
                        # Skip malformed JSON chunks - this can happen with streaming
                        continue
                    
                    # Extract chunk ID if available
                    if 'id' in data:
                        chunk_id = data['id']
                    
                    # Extract model if available
                    chunk_model = data.get('model', model)
                    
                    # Extract delta and finish_reason
                    if 'choices' in data and len(data['choices']) > 0:
                        choice = data['choices'][0]
                        delta = choice.get('delta', {})
                        finish_reason = choice.get('finish_reason')
                        
                        # Create delta object
                        content = delta.get('content')
                        role = delta.get('role')
                        
                        # On first chunk with role, include it
                        if first_chunk and role:
                            chunk_delta = ChatCompletionChunkDelta(content=content, role=role)
                            first_chunk = False
                        else:
                            chunk_delta = ChatCompletionChunkDelta(content=content)
                        
                        # Yield chunk
                        yield ChatCompletionChunk(
                            delta=chunk_delta,
                            model=chunk_model,
                            finish_reason=finish_reason,
                            chunk_id=chunk_id
                        )
                        
        except requests.RequestException as e:
            raise APIError(f"Failed to generate text stream: {str(e)}", self._get_status_code(e))
