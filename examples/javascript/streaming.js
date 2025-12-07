/**
 * Example demonstrating streaming support for text generation.
 * 
 * This script shows how to use streaming with the OpenAI-compatible API.
 */

import { Pollinations } from '@gpt4free/g4f.dev';

async function main() {
  console.log('='.repeat(70));
  console.log('Streaming Examples');
  console.log('='.repeat(70));
  
  // Initialize client
  const client = new Pollinations();
  
  // ========================================================================
  // OpenAI-Compatible Streaming API
  // ========================================================================
  
  console.log('\n1. Basic Streaming (OpenAI-compatible):');
  console.log('-'.repeat(70));
  
  const stream1 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Count to 10' }
    ],
    stream: true
  });
  
  for await (const chunk of stream1) {
    if (chunk.choices[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
  console.log('\n');
  
  console.log('\n2. Streaming with System Message:');
  console.log('-'.repeat(70));
  
  const stream2 = await client.chat.completions.create({
    messages: [
      { role: 'system', content: 'You are a creative poet.' },
      { role: 'user', content: 'Write a haiku about coding' }
    ],
    stream: true
  });
  
  for await (const chunk of stream2) {
    if (chunk.choices[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
  console.log('\n');
  
  console.log('\n3. Streaming with Temperature Control:');
  console.log('-'.repeat(70));
  
  const stream3 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Tell me a very short story about a robot' }
    ],
    temperature: 0.9,
    stream: true
  });
  
  let fullResponse = '';
  for await (const chunk of stream3) {
    const delta = chunk.choices[0]?.delta?.content;
    if (delta) {
      fullResponse += delta;
      process.stdout.write(delta);
    }
    
    // Check finish reason
    if (chunk.choices[0].finish_reason) {
      console.log(`\n\n[Finished: ${chunk.choices[0].finish_reason}]`);
    }
  }
  
  console.log(`\n[Full response length: ${fullResponse.length} characters]`);
  
  console.log('\n4. Collecting Chunks for Analysis:');
  console.log('-'.repeat(70));
  
  const stream4 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'List 5 programming languages' }
    ],
    stream: true
  });
  
  const chunks = [];
  for await (const chunk of stream4) {
    chunks.push(chunk);
    if (chunk.choices[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
  
  console.log(`\n\n[Received ${chunks.length} chunks]`);
  
  // ========================================================================
  // Advanced Use Cases
  // ========================================================================
  
  console.log('\n5. Real-time Processing:');
  console.log('-'.repeat(70));
  console.log('Simulating character-by-character display:');
  
  const stream5 = await client.chat.completions.create({
    messages: [{ role: 'user', content: 'Say "Hello World"' }],
    stream: true
  });
  
  for await (const chunk of stream5) {
    if (chunk.choices[0]?.delta?.content) {
      const content = chunk.choices[0].delta.content;
      process.stdout.write(content);
      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  }
  
  console.log('\n');
  
  console.log('\n' + '='.repeat(70));
  console.log('Streaming examples completed!');
  console.log('='.repeat(70));
}

// Run the examples
main().catch(console.error);
