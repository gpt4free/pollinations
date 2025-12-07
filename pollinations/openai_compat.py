"""OpenAI-compatible API interfaces for Pollinations."""

from typing import Optional, List, Dict, Any, Union, Iterator
import json
import requests

from .exceptions import APIError

class ImageResponseElement:
    """Element of OpenAI-compatible image generation response."""
    
    def __init__(self, url: str, revised_prompt: Optional[str] = None):
        self.url = url
        self.revised_prompt = revised_prompt

class ImageResponse:
    """OpenAI-compatible image generation response."""
    
    def __init__(self, url: str, revised_prompt: Optional[str] = None):
        self.data = [ImageResponseElement(url, revised_prompt)]
        self.created = None


class ChatCompletionMessage:
    """OpenAI-compatible chat message."""
    
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def to_dict(self):
        return {"role": self.role, "content": self.content}


class ChatCompletionChoice:
    """OpenAI-compatible chat completion choice."""
    
    def __init__(self, message: ChatCompletionMessage, finish_reason: str = "stop", index: int = 0):
        self.message = message
        self.finish_reason = finish_reason
        self.index = index


class ChatCompletion:
    """OpenAI-compatible chat completion response."""
    
    def __init__(self, content: str = None, model: Optional[str] = None, response_dict: Optional[Dict] = None):
        if response_dict:
            # Parse from API response
            self.id = response_dict.get("id", "chatcmpl-pollinations")
            self.object = response_dict.get("object", "chat.completion")
            self.created = response_dict.get("created")
            self.model = response_dict.get("model", model or "default")
            self.usage = response_dict.get("usage")
            
            # Parse choices
            choices_data = response_dict.get("choices", [])
            self.choices = []
            for choice_data in choices_data:
                message_data = choice_data.get("message", {})
                message = ChatCompletionMessage(
                    role=message_data.get("role", "assistant"),
                    content=message_data.get("content", "")
                )
                choice = ChatCompletionChoice(
                    message=message,
                    finish_reason=choice_data.get("finish_reason", "stop"),
                    index=choice_data.get("index", 0)
                )
                self.choices.append(choice)
        else:
            # Legacy: construct from plain text
            self.id = "chatcmpl-pollinations"
            self.object = "chat.completion"
            self.created = None
            self.model = model or "default"
            self.choices = [ChatCompletionChoice(ChatCompletionMessage("assistant", content))]
            self.usage = None


class ChatCompletionChunkDelta:
    """OpenAI-compatible chat completion chunk delta."""
    
    def __init__(self, content: Optional[str] = None, role: Optional[str] = None):
        self.content = content
        self.role = role


class ChatCompletionChunkChoice:
    """OpenAI-compatible chat completion chunk choice."""
    
    def __init__(self, delta: ChatCompletionChunkDelta, finish_reason: Optional[str] = None, index: int = 0):
        self.delta = delta
        self.finish_reason = finish_reason
        self.index = index


class ChatCompletionChunk:
    """OpenAI-compatible chat completion chunk for streaming."""
    
    def __init__(self, delta: ChatCompletionChunkDelta, model: Optional[str] = None, 
                 finish_reason: Optional[str] = None, chunk_id: Optional[str] = None):
        self.id = chunk_id or "chatcmpl-pollinations"
        self.object = "chat.completion.chunk"
        self.created = None
        self.model = model or "default"
        self.choices = [ChatCompletionChunkChoice(delta, finish_reason=finish_reason)]
        self.usage = None


class Images:
    """OpenAI-compatible images API."""
    
    def __init__(self, client):
        self._client = client
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        n: int = 1,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        response_format: str = "url",
        **kwargs
    ) -> ImageResponse:
        """
        Generate images using OpenAI-compatible API.
        
        Args:
            prompt: Text description of the image to generate
            model: Model name to use (optional)
            n: Number of images to generate (only 1 is supported)
            size: Image size in format "WIDTHxHEIGHT" (e.g., "1024x768")
            quality: Image quality (ignored, for compatibility)
            response_format: Response format, only "url" is supported
            **kwargs: Additional parameters passed to the underlying API
            
        Returns:
            ImageResponse with generated image URL
        """
        if n != 1:
            raise ValueError("Only n=1 is supported")
        
        if response_format != "url":
            raise ValueError("Only response_format='url' is supported")
        
        width = None
        height = None
        if size:
            parts = size.split("x")
            if len(parts) == 2:
                width = int(parts[0])
                height = int(parts[1])
        
        url = self._client.generate_image(
            prompt=prompt,
            model=model,
            width=width,
            height=height,
            **kwargs
        )

        try:
            response = requests.get(url, timeout=self._client.timeout, headers=self._client._get_headers())
            response.raise_for_status()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch image: {str(e)}")
        
        return ImageResponse(url, revised_prompt=prompt)


class ChatCompletions:
    """OpenAI-compatible chat completions API."""
    
    def __init__(self, client):
        self._client = client
    
    def create(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[ChatCompletion, Iterator[ChatCompletionChunk]]:
        """
        Create a chat completion using OpenAI-compatible API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name to use (optional)
            temperature: Sampling temperature (optional)
            max_tokens: Maximum tokens to generate (optional)
            stream: Enable streaming mode (optional)
            **kwargs: Additional parameters passed to the underlying API
            
        Returns:
            ChatCompletion with generated response (if stream=False)
            Iterator of ChatCompletionChunk (if stream=True)
        """
        from .exceptions import APIError
        
        # Build request payload
        payload = {
            "messages": messages
        }
        
        if model:
            payload["model"] = model
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if stream:
            payload["stream"] = True
            
        # Add any additional kwargs
        payload.update(kwargs)
        
        url = self._client.CHAT_URL
        headers = self._client._get_headers()
        headers["Content-Type"] = "application/json"
        
        try:
            if stream:
                # Streaming response
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self._client.timeout,
                    stream=True
                )
                response.raise_for_status()
                
                return self._parse_stream(response, model)
            else:
                # Non-streaming response
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self._client.timeout
                )
                response.raise_for_status()
                
                response_data = response.json()
                return ChatCompletion(response_dict=response_data, model=model)
                
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            raise APIError(f"Failed to create chat completion: {str(e)}", status_code)
    
    def _parse_stream(self, response, model: Optional[str] = None) -> Iterator[ChatCompletionChunk]:
        """Parse streaming response into ChatCompletionChunk objects."""
        chunk_id = None
        first_chunk = True
        
        for line in response.iter_lines():
            if not line:
                continue
            
            try:
                line_str = line.decode('utf-8')
            except UnicodeDecodeError:
                continue
            
            # SSE format: "data: {json}" or "data: [DONE]"
            if line_str.startswith('data: '):
                json_str = line_str[6:]
                
                # Check for termination signal
                if json_str.strip() == '[DONE]':
                    break
                
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError:
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


class Chat:
    """OpenAI-compatible chat API."""
    
    def __init__(self, client):
        self.completions = ChatCompletions(client)
