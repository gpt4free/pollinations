/**
 * Example demonstrating basic text generation.
 * 
 * This script shows simple text generation examples.
 */

import { Pollinations } from '@gpt4free/g4f.dev';

async function main() {
  console.log('='.repeat(70));
  console.log('Text Generation Examples');
  console.log('='.repeat(70));
  
  // Initialize client
  const client = new Pollinations();
  
  // ========================================================================
  // Basic Text Generation
  // ========================================================================
  
  console.log('\n1. Simple Question:');
  console.log('-'.repeat(70));
  const response1 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'What is the meaning of life?' }
    ]
  });
  console.log(response1.choices[0].message.content);
  
  console.log('\n2. With System Message:');
  console.log('-'.repeat(70));
  const response2 = await client.chat.completions.create({
    messages: [
      { role: 'system', content: 'You are a helpful poetry assistant.' },
      { role: 'user', content: 'Write a haiku about coding' }
    ]
  });
  console.log(response2.choices[0].message.content);
  
  console.log('\n3. With Specific Model:');
  console.log('-'.repeat(70));
  const response3 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Explain quantum computing in simple terms' }
    ],
    model: 'openai'
  });
  console.log(response3.choices[0].message.content);
  
  console.log('\n4. With Temperature Control:');
  console.log('-'.repeat(70));
  const response4 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Write a creative story opening' }
    ],
    temperature: 0.8,
    max_tokens: 100
  });
  console.log(response4.choices[0].message.content);
  
  console.log('\n5. Conversation Context:');
  console.log('-'.repeat(70));
  const response5 = await client.chat.completions.create({
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Tell me a joke.' },
      { role: 'assistant', content: 'Why do programmers prefer dark mode? Because light attracts bugs!' },
      { role: 'user', content: 'Tell me another one!' }
    ]
  });
  console.log(response5.choices[0].message.content);
  
  console.log('\n' + '='.repeat(70));
  console.log('Text generation examples completed!');
  console.log('='.repeat(70));
}

// Run the examples
main().catch(console.error);
