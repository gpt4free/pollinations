# OpenAI Compatibility Guide

This document explains the OpenAI-compatible API added to the Pollinations Python client.

## Overview

The Pollinations client now provides OpenAI-compatible interfaces that allow it to be used as a drop-in replacement for OpenAI's Python client. This means you can use familiar OpenAI API patterns while leveraging Pollinations' free AI services.

## Quick Start

```python
from pollinations import Pollinations

# Initialize client (with or without API key)
client = Pollinations()  # Free tier
# or
client = Pollinations(api_key="your-key")  # Authenticated

# Use OpenAI-compatible interfaces
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

## Chat Completions

### Basic Usage

```python
response = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)

# Access response
print(response.choices[0].message.content)
print(response.choices[0].message.role)  # 'assistant'
print(response.choices[0].finish_reason)  # 'stop'
```

### With System Message

```python
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    model="openai",
    temperature=0.7,
    max_tokens=200
)
```

### Supported Parameters

- `messages` (required): List of message dicts with 'role' and 'content'
- `model`: Model name (optional)
- `temperature`: Sampling temperature 0-1 (optional)
- `max_tokens`: Maximum tokens to generate (optional)
- `stream`: Enable streaming mode (optional, default: False)
- `seed`: Random seed for reproducibility (optional)
- `json`: Enable JSON output (optional)
- `tools`: List of tools/functions the model can call (optional) **NEW!**
- `tool_choice`: Controls which tool is called (optional) **NEW!**
- `reasoning_effort`: Level of reasoning - "low", "medium", "high" (optional) **NEW!**

### Tool Calls (Function Calling) **NEW!**

Tool calls allow the model to use external functions to answer questions.

#### Defining Tools

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools
)

# Check for tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        print(f"Function: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

#### Tool Choice

Control which tools the model can use:

```python
# Auto (default) - model decides
tool_choice="auto"

# Force tool use
tool_choice="required"

# Disable tools
tool_choice="none"

# Force specific tool
tool_choice={"type": "function", "function": {"name": "get_weather"}}
```

### Reasoning Support **NEW!**

Access the model's chain-of-thought reasoning process.

**Key Concepts:**
- **`reasoning_effort`** (request parameter): Optional parameter to control reasoning level. Values: "low", "medium", "high". *Note: May not be supported by all Pollinations endpoints.*
- **`reasoning_content`** (response field): Contains the model's actual reasoning/thinking process when available.

```python
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Solve: 15 * 24"}],
    reasoning_effort="high"  # Optional: "low", "medium", or "high"
                             # May not be supported by all endpoints
)

# Access reasoning (if provided by the model)
if response.choices[0].message.reasoning_content:
    print(f"Reasoning: {response.choices[0].message.reasoning_content}")
print(f"Answer: {response.choices[0].message.content}")
```

**Note:** Some models may automatically provide `reasoning_content` in responses without requiring the `reasoning_effort` parameter. The availability depends on the model being used.

### Streaming Support

Streaming allows you to receive the response in real-time as it's being generated.

#### Basic Streaming

```python
stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

#### Advanced Streaming

```python
stream = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a creative writer."},
        {"role": "user", "content": "Write a poem about AI"}
    ],
    model="openai",
    temperature=0.8,
    stream=True
)

full_response = ""
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        full_response += delta
        print(delta, end="", flush=True)
    
    # Check if streaming is complete
    if chunk.choices[0].finish_reason:
        print(f"\n\nFinished: {chunk.choices[0].finish_reason}")
```

### Response Structure

**Non-streaming (stream=False):**

```python
ChatCompletion(
    id="chatcmpl-pollinations",
    object="chat.completion",
    created=None,
    model="openai",
    choices=[
        ChatCompletionChoice(
            index=0,
            message=ChatCompletionMessage(
                role="assistant",
                content="Generated response text...",
                tool_calls=[  # Present when model requests tool calls
                    ToolCall(
                        id="call_123",
                        type="function",
                        function=Function(
                            name="get_weather",
                            arguments='{"location": "Paris"}'
                        )
                    )
                ],
                reasoning_content="Step-by-step reasoning..."  # Present with reasoning_effort
            ),
            finish_reason="stop"  # or "tool_calls" when requesting tools
        )
    ],
    usage=None
)
```

**Streaming (stream=True):**

Each chunk is a `ChatCompletionChunk`:

```python
ChatCompletionChunk(
    id="chatcmpl-pollinations",
    object="chat.completion.chunk",
    created=None,
    model="openai",
    choices=[
        ChatCompletionChunkChoice(
            index=0,
            delta=ChatCompletionChunkDelta(
                content="text chunk...",
                role="assistant",  # Only in first chunk
                tool_calls=[...],  # Present when streaming tool calls
                reasoning_content="reasoning chunk..."  # Present when streaming reasoning
            ),
            finish_reason=None  # "stop" in final chunk
        )
    ],
    usage=None
)
```

## Image Generation

### Basic Usage

```python
response = client.images.generate(
    prompt="A beautiful sunset over mountains"
)

# Access image URL
image_url = response.data[0]["url"]
```

### With Size and Model

```python
response = client.images.generate(
    prompt="A futuristic city at night",
    size="1024x768",
    model="flux"
)

print(response.data[0]["url"])
print(response.data[0]["revised_prompt"])
```

### Supported Parameters

- `prompt` (required): Text description of the image
- `model`: Model name (optional)
- `size`: Image size as "WIDTHxHEIGHT" (e.g., "1024x768")
- `n`: Number of images (must be 1)
- `response_format`: Must be "url" (default)
- Additional parameters: `seed`, `nologo`, `private`, `enhance`

### Response Structure

```python
ImageResponse(
    data=[
        {
            "url": "https://image.pollinations.ai/prompt/...",
            "revised_prompt": "Original prompt text"
        }
    ],
    created=None
)
```

## API Key Support

### Without API Key (Free Tier)

```python
client = Pollinations()
# Uses: image.pollinations.ai and text.pollinations.ai
```

### With API Key (Authenticated)

```python
client = Pollinations(api_key="your-api-key-here")
# Uses: gen.pollinations.ai endpoints
# API key sent as: Authorization: Bearer your-api-key-here
```

Authenticated endpoints may provide:
- Higher rate limits
- Additional features
- Priority processing

## Migration from OpenAI

### Before (OpenAI)

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

# Chat
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)

# Images
response = client.images.generate(
    prompt="A sunset",
    size="1024x1024"
)
```

### After (Pollinations)

```python
from pollinations import Pollinations

client = Pollinations(api_key="optional-key")  # Free without key!

# Chat - same interface!
response = client.chat.completions.create(
    model="openai",
    messages=[{"role": "user", "content": "Hello"}]
)

# Streaming - same interface!
stream = client.chat.completions.create(
    model="openai",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# Images - same interface!
response = client.images.generate(
    prompt="A sunset",
    size="1024x1024"
)
```

## Limitations

### Chat Completions
- ✅ Streaming (`stream=True`) fully supported
- ✅ All standard parameters supported

### Image Generation
- ❌ Only `n=1` supported (single image at a time)
- ❌ Only `response_format="url"` supported
- ✅ All size formats supported
- ✅ Multiple models supported

## Comparison: Native vs OpenAI-Compatible API

Both APIs access the same underlying Pollinations services:

```python
# Native API
text = client.generate_text("Hello")
image_url = client.generate_image("Sunset", width=512, height=512)

# OpenAI-compatible API
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}]
)
text = response.choices[0].message.content

response = client.images.generate("Sunset", size="512x512")
image_url = response.data[0]["url"]
```

Choose based on your preference:
- **Native API**: Simpler, more direct
- **OpenAI-compatible API**: Familiar if coming from OpenAI, easier migration

## Examples

See `examples/openai_compatible.py` for comprehensive examples of:
- Basic chat completions
- Chat with system messages
- Temperature and parameter control
- Image generation with various options
- Side-by-side comparison of both APIs

## Testing

Run the OpenAI compatibility tests:

```bash
python -m unittest tests/test_openai_compat.py -v
```

All 14 OpenAI compatibility tests validate:
- Interface availability
- API key handling
- Parameter validation
- Response structure
- Error handling

## Support

For issues or questions:
- GitHub Issues: https://github.com/gpt4free/pollinations/issues
- Examples: `examples/openai_compatible.py`
- Tests: `tests/test_openai_compat.py`
