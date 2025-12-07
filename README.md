# Pollinations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/pollinations-client.svg)](https://badge.fury.io/py/pollinations-client)

A Python wrapper for [Pollinations AI](https://pollinations.ai/) - Free text and image generation APIs.

Pollinations provides free, unlimited access to various AI models for text and image generation without requiring API keys.

## Features

- 🎨 **Image Generation**: Create images from text descriptions
- 💬 **Text Generation**: Generate text using various language models
- 🌊 **Streaming Support**: Stream text responses in real-time
- 🛠️ **Tool Calls**: Function calling support for agentic workflows (NEW!)
- 🧠 **Reasoning**: Chain-of-thought reasoning with reasoning models (NEW!)
- 🔄 **No API Key Required**: Completely free to use (API key optional for advanced features)
- 🚀 **Simple API**: Easy-to-use interface with both native and OpenAI-compatible APIs
- 🎯 **Multiple Models**: Access to various AI models
- ⚡ **Fast**: Direct API access with minimal overhead
- 🔌 **OpenAI Compatible**: Drop-in replacement for OpenAI API (`client.chat.completions.create()`, `client.images.generate()`)

## Installation

Install from PyPI:

```bash
pip install pollinations-client
```

Or install from source:

```bash
git clone https://github.com/gpt4free/pollinations.git
cd pollinations
pip install -e .
```

## Quick Start

### OpenAI-Compatible API (Recommended)

```python
from pollinations import Pollinations

# Create a client (no API key required for free tier)
client = Pollinations()

# Or with API key for gen.pollinations.ai
# client = Pollinations(api_key="your-api-key")

# Chat completion (OpenAI-compatible)
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ],
    model="openai",
    temperature=0.7
)
print(response.choices[0].message.content)

# Streaming chat completion
stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

# Tool calls (function calling) - NEW!
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
}]
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools
)
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"Tool: {tool_call.function.name}, Args: {tool_call.function.arguments}")

# Reasoning - NEW!
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Solve: 15 * 24"}],
    reasoning_effort="high"
)
if response.choices[0].message.reasoning_content:
    print(f"Reasoning: {response.choices[0].message.reasoning_content}")
print(f"Answer: {response.choices[0].message.content}")

# Image generation (OpenAI-compatible)
response = client.images.generate(
    prompt="A serene mountain landscape at sunset",
    size="1024x768",
    model="flux"
)
print(response.data[0]["url"])
```

### Native API

#### Text Generation

```python
from pollinations import Pollinations

# Create a client
client = Pollinations()

# Generate text
response = client.generate_text("What is the meaning of life?")
print(response)

# Use a specific model
response = client.generate_text(
    "Explain quantum computing",
    model="openai"
)
print(response)

# With system message and temperature
response = client.generate_text(
    "Write a haiku about coding",
    system="You are a helpful poetry assistant",
    temperature=0.8
)
print(response)
```

### Image Generation

```python
from pollinations import Pollinations

# Create a client
client = Pollinations()

# Generate image (returns URL)
image_url = client.generate_image("A beautiful sunset over mountains")
print(f"Image URL: {image_url}")

# Generate with specific model and dimensions
image_url = client.generate_image(
    "A futuristic city at night",
    model="flux",
    width=1024,
    height=768
)

# Download image to file
client.download_image(
    "A cute cat wearing sunglasses",
    "cat.png",
    width=512,
    height=512
)
```

## API Reference

### Pollinations Client

#### `__init__(timeout=30, api_key=None)`

Create a new Pollinations client.

**Parameters:**
- `timeout` (int): Request timeout in seconds (default: 30)
- `api_key` (str, optional): API key for gen.pollinations.ai (enables authenticated endpoints)

### OpenAI-Compatible API

The client provides OpenAI-compatible interfaces that can be used as drop-in replacements for OpenAI's API.

#### `client.chat.completions.create(messages, model=None, temperature=None, max_tokens=None, stream=False, tools=None, tool_choice=None, reasoning_effort=None, **kwargs)`

Create a chat completion (OpenAI-compatible).

**Parameters:**
- `messages` (list): List of message dicts with 'role' and 'content'
- `model` (str, optional): Model name to use
- `temperature` (float, optional): Sampling temperature 0-1
- `max_tokens` (int, optional): Maximum tokens to generate
- `stream` (bool): Enable streaming mode (default: False)
- `tools` (list, optional): List of tools/functions the model can call
- `tool_choice` (str or dict, optional): Controls which tool is called ("auto", "none", or specific tool)
- `reasoning_effort` (str, optional): Level of reasoning ("low", "medium", "high"). Note: May not be supported by all endpoints

**Returns:** 
- ChatCompletion object with `choices[0].message.content` (if stream=False)
- Iterator of ChatCompletionChunk objects (if stream=True)

**Response fields:**
- `choices[0].message.content`: The generated text response
- `choices[0].message.tool_calls`: List of tool calls requested by the model (if any)
- `choices[0].message.reasoning_content`: The model's reasoning process (if available from the model)

#### `client.images.generate(prompt, model=None, size=None, n=1, **kwargs)`

Generate images (OpenAI-compatible).

**Parameters:**
- `prompt` (str): Text description of the image
- `model` (str, optional): Model name to use
- `size` (str, optional): Image size in format "WIDTHxHEIGHT" (e.g., "1024x768")
- `n` (int): Number of images (must be 1)
- `response_format` (str): Must be "url"

**Returns:** ImageResponse object with `data[0]["url"]`

### Native API

#### `generate_text(prompt, model=None, system=None, temperature=None, max_tokens=None, seed=None, json=False)`

Generate text using a language model.

**Parameters:**
- `prompt` (str): Input text prompt
- `model` (str, optional): Model name to use
- `system` (str, optional): System message to set context
- `temperature` (float, optional): Sampling temperature 0-1 (higher = more creative)
- `max_tokens` (int, optional): Maximum tokens to generate
- `seed` (int, optional): Random seed for reproducibility
- `json` (bool): If True, output will be formatted as JSON

**Returns:** Generated text (str)

#### `generate_image(prompt, model=None, width=None, height=None, seed=None, nologo=False, private=False, enhance=False, negative_prompt=None, quality=None, transparent=False, guidance_scale=None, nofeed=False, safe=False, image=None, duration=None, aspect_ratio=None, audio=False)`

Generate an image or video from a text prompt.

**Parameters:**
- `prompt` (str): Text description of the image to generate
- `model` (str, optional): Model name to use
- `width` (int, optional): Image width in pixels
- `height` (int, optional): Image height in pixels
- `seed` (int, optional): Random seed for reproducibility
- `nologo` (bool): If True, removes Pollinations logo from image
- `private` (bool): If True, image won't be published to feed
- `enhance` (bool): If True, automatically enhances the prompt
- `negative_prompt` (str, optional): What to avoid in the generated image
- `quality` (str, optional): Image quality level - "low", "medium", "high", or "hd"
- `transparent` (bool): If True, generates with transparent background
- `guidance_scale` (float, optional): How closely to follow the prompt (1-20)
- `nofeed` (bool): If True, don't add to public feed
- `safe` (bool): If True, enable safety content filters
- `image` (str, optional): Reference image URL(s) for image-to-image. Comma/pipe separated for multiple
- `duration` (int, optional): Video duration in seconds (for video models)
- `aspect_ratio` (str, optional): Video aspect ratio - "16:9" or "9:16" (for video models)
- `audio` (bool): If True, enable audio generation for video (veo only)

**Returns:** URL of the generated image (str)

#### `download_image(prompt, output_path, **kwargs)`

Generate and download an image to a local file.

**Note:** Video-specific parameters (duration, aspect_ratio, audio) are not supported for downloads as they generate video files which should be accessed via URLs.

**Parameters:**
- `prompt` (str): Text description of the image to generate
- `output_path` (str): Local path where the image will be saved
- `**kwargs`: Same image parameters as `generate_image()` (excluding video-specific parameters)

**Returns:** Path to the saved image file (str)

#### `get_image_models(force_refresh=False)`

Get list of available image generation models.

**Returns:** List of model names

#### `get_text_models(force_refresh=False)`

Get list of available text generation models.

**Returns:** List of model information dictionaries

## Tool Calls (Function Calling)

Tool calls enable the model to use external functions/tools to answer questions or perform tasks.

### Defining Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Using Tool Calls

```python
# Request with tools
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools
)

# Check if model wants to call a tool
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        print(f"Function: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
        # Execute the function and send results back
```

### Controlling Tool Choice

```python
# Let model decide (default)
tool_choice="auto"

# Force model to use tools
tool_choice="required"

# Prevent tool use
tool_choice="none"

# Force specific tool
tool_choice={"type": "function", "function": {"name": "get_weather"}}
```

## Reasoning

Reasoning models expose their chain-of-thought process, showing how they arrived at an answer.

**Important distinction:**
- **`reasoning_effort`** (request parameter): Controls the level of reasoning - "low", "medium", "high". *Note: This parameter may not be supported by all Pollinations endpoints. The API will return an error if unsupported.*
- **`reasoning_content`** (response field): Contains the model's actual reasoning/thinking process

### Using Reasoning

```python
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Calculate the factorial of 5"}],
    reasoning_effort="high"  # Optional: "low", "medium", "high"
                             # May not be supported by all endpoints
)

# Access reasoning process (if provided by the model)
if response.choices[0].message.reasoning_content:
    print(f"Reasoning: {response.choices[0].message.reasoning_content}")
print(f"Answer: {response.choices[0].message.content}")
```

**Note:** Some models automatically provide `reasoning_content` without needing the `reasoning_effort` parameter. The availability of this feature depends on the specific model and endpoint being used.

### Streaming with Reasoning

```python
stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Solve this problem"}],
    reasoning_effort="medium",  # Optional, may not be supported
    stream=True
)

for chunk in stream:
    # Reasoning tokens (if provided by model)
    if chunk.choices[0].delta.reasoning_content:
        print(f"[Reasoning] {chunk.choices[0].delta.reasoning_content}")
    
    # Answer tokens
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Examples

### Python Examples

See the [examples](examples/) directory for Python usage examples:

- [OpenAI-Compatible API](examples/openai_compatible.py) - OpenAI-compatible interface examples
- [Tool Calls and Reasoning](examples/tool_calls_and_reasoning.py) - **NEW!** Function calling and reasoning examples
- [Streaming Examples](examples/streaming.py) - Real-time streaming text generation
- [Text Generation Examples](examples/text_generation.py)
- [Image Generation Examples](examples/image_generation.py)
- [List Models](examples/list_models.py)

### JavaScript Examples

JavaScript/Node.js examples using the `@gpt4free/g4f.dev` client are available in [examples/javascript](examples/javascript/):

- [OpenAI-Compatible API](examples/javascript/openai_compatible.js) - OpenAI-compatible interface examples
- [Tool Calls and Reasoning](examples/javascript/tool_calls_and_reasoning.js) - Function calling and reasoning examples
- [Streaming Examples](examples/javascript/streaming.js) - Real-time streaming text generation
- [Text Generation Examples](examples/javascript/text_generation.js) - Basic text generation
- [Image Generation Examples](examples/javascript/image_generation.js) - Image generation with various models

See the [JavaScript README](examples/javascript/README.md) for installation and usage instructions.

## API Key Support

The client supports optional API keys from https://enter.pollinations.ai:

```python
# Without API key (free tier, uses image.pollinations.ai and text.pollinations.ai)
client = Pollinations()

# With API key (uses gen.pollinations.ai endpoints)
client = Pollinations(api_key="your-api-key-here")
```

When an API key is provided:
- Requests use authenticated endpoints (`gen.pollinations.ai`)
- API key is sent in the `Authorization` header as a Bearer token
- May provide access to additional features or higher rate limits

## Error Handling

```python
from pollinations import Pollinations, APIError, ModelNotFoundError

client = Pollinations()

try:
    response = client.generate_text("Hello!")
except APIError as e:
    print(f"API Error: {e}")
    if e.status_code:
        print(f"Status Code: {e.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Requirements

- Python 3.7+
- requests >= 2.31.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is an unofficial wrapper for Pollinations AI. For official information about the service, visit [pollinations.ai](https://pollinations.ai/).

## Related Projects

- [pollinations](https://github.com/pollinations/pollinations) - Open-Source Gen-AI Platform
- [gpt4free](https://github.com/xtekky/gpt4free) - Collection of free AI APIs
- [gpt4free/g4f.dev](https://github.com/gpt4free/g4f.dev) - Free AI endpoints

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/gpt4free/pollinations/issues) on GitHub.