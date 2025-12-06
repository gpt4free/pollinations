# Polinations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A Python wrapper for [Polinations AI](https://pollinations.ai/) - Free text and image generation APIs.

Polinations provides free, unlimited access to various AI models for text and image generation without requiring API keys.

## Features

- 🎨 **Image Generation**: Create images from text descriptions
- 💬 **Text Generation**: Generate text using various language models
- 🔄 **No API Key Required**: Completely free to use
- 🚀 **Simple API**: Easy-to-use interface
- 🎯 **Multiple Models**: Access to various AI models
- ⚡ **Fast**: Direct API access with minimal overhead

## Installation

```bash
pip install -r requirements.txt
```

Or install from source:

```bash
git clone https://github.com/gpt4free/polinations.git
cd polinations
pip install -e .
```

## Quick Start

### Text Generation

```python
from polinations import Polinations

# Create a client
client = Polinations()

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
from polinations import Polinations

# Create a client
client = Polinations()

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

### Polinations Client

#### `__init__(timeout=30)`

Create a new Polinations client.

**Parameters:**
- `timeout` (int): Request timeout in seconds (default: 30)

#### `generate_text(prompt, model=None, system=None, temperature=None, max_tokens=None, seed=None, jsonMode=False)`

Generate text using a language model.

**Parameters:**
- `prompt` (str): Input text prompt
- `model` (str, optional): Model name to use
- `system` (str, optional): System message to set context
- `temperature` (float, optional): Sampling temperature 0-1 (higher = more creative)
- `max_tokens` (int, optional): Maximum tokens to generate
- `seed` (int, optional): Random seed for reproducibility
- `jsonMode` (bool): If True, output will be formatted as JSON

**Returns:** Generated text (str)

#### `generate_image(prompt, model=None, width=None, height=None, seed=None, nologo=False, private=False, enhance=False)`

Generate an image from a text prompt.

**Parameters:**
- `prompt` (str): Text description of the image to generate
- `model` (str, optional): Model name to use
- `width` (int, optional): Image width in pixels
- `height` (int, optional): Image height in pixels
- `seed` (int, optional): Random seed for reproducibility
- `nologo` (bool): If True, removes Polinations logo from image
- `private` (bool): If True, image won't be published to feed
- `enhance` (bool): If True, automatically enhances the prompt

**Returns:** URL of the generated image (str)

#### `download_image(prompt, output_path, **kwargs)`

Generate and download an image to a local file.

**Parameters:**
- `prompt` (str): Text description of the image to generate
- `output_path` (str): Local path where the image will be saved
- `**kwargs`: Same parameters as `generate_image()`

**Returns:** Path to the saved image file (str)

#### `get_image_models(force_refresh=False)`

Get list of available image generation models.

**Returns:** List of model names

#### `get_text_models(force_refresh=False)`

Get list of available text generation models.

**Returns:** List of model information dictionaries

## Examples

See the [examples](examples/) directory for more usage examples:

- [Text Generation Examples](examples/text_generation.py)
- [Image Generation Examples](examples/image_generation.py)
- [List Models](examples/list_models.py)

## Error Handling

```python
from polinations import Polinations, APIError, ModelNotFoundError

client = Polinations()

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

This is an unofficial wrapper for Polinations AI. For official information about the service, visit [pollinations.ai](https://pollinations.ai/).

## Related Projects

- [gpt4free](https://github.com/xtekky/gpt4free) - Collection of free AI APIs
- [g4f.dev](https://github.com/gpt4free/g4f.dev) - Free AI endpoints

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/gpt4free/polinations/issues) on GitHub.