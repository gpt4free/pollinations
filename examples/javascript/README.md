# JavaScript Client Examples for Pollinations

These examples demonstrate how to use the Pollinations API with JavaScript/Node.js using the `@gpt4free/g4f.dev` client.

## Installation

```bash
npm install @gpt4free/g4f.dev
```

## Available Examples

- **openai_compatible.js** - OpenAI-compatible API usage for chat completions and image generation
- **streaming.js** - Real-time streaming text generation examples
- **image_generation.js** - Image generation with various models and options
- **tool_calls_and_reasoning.js** - Function calling and reasoning examples
- **text_generation.js** - Basic text generation examples

## Running the Examples

Each example can be run with Node.js:

```bash
node openai_compatible.js
node streaming.js
node image_generation.js
node tool_calls_and_reasoning.js
node text_generation.js
```

## Browser Usage

For browser usage, you can use the same API with appropriate bundlers (webpack, vite, etc.):

```javascript
import { Pollinations } from '@gpt4free/g4f.dev';

const client = new Pollinations({ apiKey: 'optional' });

// For image generation in browser
const result = await client.images.generate({
  model: 'flux',
  prompt: 'A futuristic city skyline at night',
  size: '512x512'
});

const image = new Image();
image.src = result.data[0].url;
document.body.appendChild(image);
```

## API Key (Optional)

The Pollinations API works without an API key for free tier access. To use authenticated endpoints:

```javascript
const client = new Pollinations({ apiKey: 'your-api-key-here' });
```

## Documentation

For more information, see:
- [Pollinations Documentation](https://pollinations.ai/)
- [g4f.dev Client Documentation](https://github.com/gpt4free/g4f.dev/blob/main/docs/client_js.md)
