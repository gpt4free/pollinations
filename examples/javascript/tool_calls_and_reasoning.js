/**
 * Example demonstrating tool calls (function calling) and reasoning features.
 * 
 * This script shows how to use function calling and reasoning capabilities.
 */

import { Pollinations } from '@gpt4free/g4f.dev';

async function main() {
  console.log('='.repeat(70));
  console.log('Tool Calls and Reasoning Examples');
  console.log('='.repeat(70));
  
  // Initialize client
  const client = new Pollinations();
  
  // ========================================================================
  // Function Calling / Tool Calls
  // ========================================================================
  
  console.log('\n1. Basic Tool Call:');
  console.log('-'.repeat(70));
  
  const tools = [
    {
      type: 'function',
      function: {
        name: 'get_weather',
        description: 'Get the current weather for a location',
        parameters: {
          type: 'object',
          properties: {
            location: {
              type: 'string',
              description: 'City name'
            },
            unit: {
              type: 'string',
              enum: ['celsius', 'fahrenheit'],
              description: 'Temperature unit'
            }
          },
          required: ['location']
        }
      }
    }
  ];
  
  const response1 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: "What's the weather in Paris?" }
    ],
    tools: tools
  });
  
  if (response1.choices[0].message.tool_calls) {
    const toolCall = response1.choices[0].message.tool_calls[0];
    console.log(`Tool Called: ${toolCall.function.name}`);
    console.log(`Arguments: ${toolCall.function.arguments}`);
  } else {
    console.log(`Response: ${response1.choices[0].message.content}`);
  }
  
  console.log('\n2. Multiple Tools:');
  console.log('-'.repeat(70));
  
  const multipleTools = [
    {
      type: 'function',
      function: {
        name: 'get_weather',
        description: 'Get the current weather',
        parameters: {
          type: 'object',
          properties: {
            location: { type: 'string' }
          },
          required: ['location']
        }
      }
    },
    {
      type: 'function',
      function: {
        name: 'search_web',
        description: 'Search the web for information',
        parameters: {
          type: 'object',
          properties: {
            query: { type: 'string' }
          },
          required: ['query']
        }
      }
    },
    {
      type: 'function',
      function: {
        name: 'calculate',
        description: 'Perform mathematical calculations',
        parameters: {
          type: 'object',
          properties: {
            expression: { type: 'string' }
          },
          required: ['expression']
        }
      }
    }
  ];
  
  const response2 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Calculate 15 * 24' }
    ],
    tools: multipleTools
  });
  
  if (response2.choices[0].message.tool_calls) {
    response2.choices[0].message.tool_calls.forEach((toolCall, idx) => {
      console.log(`Tool ${idx + 1}: ${toolCall.function.name}`);
      console.log(`Arguments: ${toolCall.function.arguments}`);
    });
  } else {
    console.log(`Response: ${response2.choices[0].message.content}`);
  }
  
  console.log('\n3. Tool Choice Control:');
  console.log('-'.repeat(70));
  
  // Force the model to use a specific tool
  const response3 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: "What's the temperature in Tokyo?" }
    ],
    tools: tools,
    tool_choice: { type: 'function', function: { name: 'get_weather' } }
  });
  
  if (response3.choices[0].message.tool_calls) {
    console.log('Forced tool call succeeded:');
    console.log(`Tool: ${response3.choices[0].message.tool_calls[0].function.name}`);
  }
  
  // ========================================================================
  // Reasoning
  // ========================================================================
  
  console.log('\n4. Basic Reasoning:');
  console.log('-'.repeat(70));
  
  const response4 = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Solve: 15 * 24' }
    ],
    reasoning_effort: 'high'
  });
  
  if (response4.choices[0].message.reasoning_content) {
    console.log(`Reasoning: ${response4.choices[0].message.reasoning_content}`);
  }
  console.log(`Answer: ${response4.choices[0].message.content}`);
  
  console.log('\n5. Reasoning with Different Effort Levels:');
  console.log('-'.repeat(70));
  
  const effortLevels = ['low', 'medium', 'high'];
  
  for (const effort of effortLevels) {
    console.log(`\nEffort Level: ${effort}`);
    const response = await client.chat.completions.create({
      messages: [
        { role: 'user', content: 'Calculate the factorial of 5' }
      ],
      reasoning_effort: effort
    });
    
    if (response.choices[0].message.reasoning_content) {
      console.log(`Reasoning: ${response.choices[0].message.reasoning_content.substring(0, 100)}...`);
    }
    console.log(`Answer: ${response.choices[0].message.content}`);
  }
  
  console.log('\n6. Streaming with Reasoning:');
  console.log('-'.repeat(70));
  
  const stream = await client.chat.completions.create({
    messages: [
      { role: 'user', content: 'Solve this problem: What is 123 + 456?' }
    ],
    reasoning_effort: 'medium',
    stream: true
  });
  
  let hasReasoning = false;
  for await (const chunk of stream) {
    // Reasoning tokens
    if (chunk.choices[0]?.delta?.reasoning_content) {
      if (!hasReasoning) {
        console.log('\n[Reasoning]:');
        hasReasoning = true;
      }
      process.stdout.write(chunk.choices[0].delta.reasoning_content);
    }
    
    // Answer tokens
    if (chunk.choices[0]?.delta?.content) {
      if (hasReasoning) {
        console.log('\n\n[Answer]:');
        hasReasoning = false;
      }
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
  
  console.log('\n');
  
  console.log('\n7. Complete Function Calling Workflow:');
  console.log('-'.repeat(70));
  
  // Simulated function execution
  function executeFunction(name, argsStr) {
    const args = JSON.parse(argsStr);
    
    if (name === 'get_weather') {
      return JSON.stringify({
        location: args.location,
        temperature: 22,
        condition: 'sunny',
        unit: args.unit || 'celsius'
      });
    }
    return null;
  }
  
  // First request with tools
  const initialResponse = await client.chat.completions.create({
    messages: [
      { role: 'user', content: "What's the weather like in London?" }
    ],
    tools: tools
  });
  
  if (initialResponse.choices[0].message.tool_calls) {
    const toolCall = initialResponse.choices[0].message.tool_calls[0];
    console.log(`Model requested: ${toolCall.function.name}(${toolCall.function.arguments})`);
    
    // Execute the function
    const functionResult = executeFunction(toolCall.function.name, toolCall.function.arguments);
    console.log(`Function returned: ${functionResult}`);
    
    // Send result back to model
    const messages = [
      { role: 'user', content: "What's the weather like in London?" },
      initialResponse.choices[0].message,
      {
        role: 'tool',
        tool_call_id: toolCall.id,
        content: functionResult
      }
    ];
    
    const finalResponse = await client.chat.completions.create({
      messages: messages,
      tools: tools
    });
    
    console.log(`Final Response: ${finalResponse.choices[0].message.content}`);
  }
  
  console.log('\n' + '='.repeat(70));
  console.log('Tool calls and reasoning examples completed!');
  console.log('='.repeat(70));
}

// Run the examples
main().catch(console.error);
