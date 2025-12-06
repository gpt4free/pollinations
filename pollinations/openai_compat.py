"""OpenAI-compatible API interfaces for Polinations."""

from typing import Optional, List, Dict, Any, Union, Iterator
import json


class ImageResponse:
    """OpenAI-compatible image generation response."""
    
    def __init__(self, url: str, revised_prompt: Optional[str] = None):
        self.data = [{"url": url, "revised_prompt": revised_prompt}]
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
    
    def __init__(self, content: str, model: Optional[str] = None):
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
        # Extract system message and user prompt
        system = None
        prompt = None
        
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            elif msg["role"] == "user":
                prompt = msg["content"]
        
        if not prompt:
            raise ValueError("At least one user message is required")
        
        # Extract seed and jsonMode from kwargs if present
        seed = kwargs.pop("seed", None)
        jsonMode = kwargs.pop("json_mode", False) or kwargs.pop("jsonMode", False)
        
        if stream:
            # Return streaming iterator
            return self._client.generate_text_stream(
                prompt=prompt,
                model=model,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                seed=seed,
                jsonMode=jsonMode,
                **kwargs
            )
        else:
            # Return complete response
            response = self._client.generate_text(
                prompt=prompt,
                model=model,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                seed=seed,
                jsonMode=jsonMode,
                **kwargs
            )
            
            return ChatCompletion(response, model=model)


class Chat:
    """OpenAI-compatible chat API."""
    
    def __init__(self, client):
        self.completions = ChatCompletions(client)
