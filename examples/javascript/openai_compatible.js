/**
 * Example demonstrating OpenAI-compatible API usage.
 * 
 * This script shows how to use the OpenAI-compatible interface for both
 * chat completions and image generation.
 */

import { Pollinations } from '@gpt4free/g4f.dev';

async function main() {
  console.log('='.repeat(70));
  console.log('OpenAI-Compatible API Examples');
  console.log('='.repeat(70));
  
  // Initialize client (with or without API key)
  // Without API key (uses free public API)
  const client = new Pollinations();
  
  // With API key (uses gen.pollinations.ai)
  // const client = new Pollinations({ apiKey: 'your-api-key-here' });
  
  // ========================================================================
  // Chat Completions API (OpenAI-compatible)
  // ========================================================================
  
  console.log('\n1. Simple Chat Completion:');
  console.log('-'.repeat(70));
  const response1 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'What is JavaScript?' }
    ]
  });
  console.log(`Response: ${response1.choices[0].message.content}`);
  
  console.log('\n2. Chat with System Message:');
  console.log('-'.repeat(70));
  const response2 = await client.chat.completions.create({
    messages: [
      { role: 'system', content: 'You are a helpful coding assistant.' },
      { role: 'user', content: 'Explain async/await in JavaScript' }
    ],
    model: 'openai'
  });
  console.log(`Response: ${response2.choices[0].message.content}`);
  
  console.log('\n3. Chat with Temperature Control:');
  console.log('-'.repeat(70));
  const response3 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Write a creative story about a robot' }
    ],
    temperature: 0.9,
    max_tokens: 200
  });
  console.log(`Response: ${response3.choices[0].message.content}`);
  
  console.log('\n4. Accessing Response Fields:');
  console.log('-'.repeat(70));
  const response4 = await client.chat.completions.create({
    messages: [{ role: 'user', content: 'Hello!' }],
    model: 'openai'
  });
  console.log(`Object Type: ${response4.object}`);
  console.log(`Model: ${response4.model}`);
  console.log(`Finish Reason: ${response4.choices[0].finish_reason}`);
  console.log(`Message Role: ${response4.choices[0].message.role}`);
  console.log(`Message Content: ${response4.choices[0].message.content}`);
  
  // ========================================================================
  // Images API (OpenAI-compatible)
  // ========================================================================
  
  console.log('\n5. Simple Image Generation:');
  console.log('-'.repeat(70));
  const imgResponse1 = await client.images.generate({
    prompt: 'A serene mountain landscape at sunset'
  });
  console.log(`Image URL: ${imgResponse1.data[0].url}`);
  
  console.log('\n6. Image with Size:');
  console.log('-'.repeat(70));
  const imgResponse2 = await client.images.generate({
    prompt: 'A futuristic city skyline',
    size: '1024x768'
  });
  console.log(`Image URL: ${imgResponse2.data[0].url.substring(0, 80)}...`);
  
  console.log('\n7. Image with Model:');
  console.log('-'.repeat(70));
  const imgResponse3 = await client.images.generate({
    prompt: 'Abstract art with vibrant colors',
    model: 'flux',
    size: '512x512'
  });
  console.log(`Image URL: ${imgResponse3.data[0].url.substring(0, 80)}...`);
  console.log(`Revised Prompt: ${imgResponse3.data[0].revised_prompt}`);
  
  console.log('\n' + '='.repeat(70));
  console.log('OpenAI-compatible API works perfectly!');
  console.log('='.repeat(70));
}

// Run the examples
main().catch(console.error);
