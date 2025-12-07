"""
Example demonstrating tool calls and reasoning support.

This script shows how to use the new tool calls (function calling) and
reasoning features in the OpenAI-compatible API.
"""

from pollinations import Pollinations
import json

# Constants for formatting
SEPARATOR_WIDTH = 70


def main():
    print("=" * SEPARATOR_WIDTH)
    print("Tool Calls and Reasoning Examples")
    print("=" * SEPARATOR_WIDTH)
    
    # Initialize client
    client = Pollinations()
    
    # ========================================================================
    # Tool Calls (Function Calling) Examples
    # ========================================================================
    
    print("\n1. Using Tool Calls (Function Calling):")
    print("-" * SEPARATOR_WIDTH)
    
    # Define tools (functions) that the model can use
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
                            "description": "The city name, e.g., 'London' or 'San Francisco'"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Temperature unit"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    # Example 1: Basic tool call request
    print("\nExample 1a: Requesting a tool call")
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant with access to weather and web search tools."},
            {"role": "user", "content": "What's the weather like in Paris?"}
        ],
        tools=tools,
        model="openai"
    )
    
    print(f"Response finish reason: {response.choices[0].finish_reason}")
    if response.choices[0].message.tool_calls:
        print("Tool calls requested:")
        for tool_call in response.choices[0].message.tool_calls:
            print(f"  - Function: {tool_call.function.name}")
            print(f"    Arguments: {tool_call.function.arguments}")
    else:
        print(f"Response: {response.choices[0].message.content}")
    
    # Example 2: Forcing a specific tool
    print("\nExample 1b: Forcing a specific tool with tool_choice")
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Tell me about Python programming"}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "search_web"}},
        model="openai"
    )
    
    if response.choices[0].message.tool_calls:
        print("Forced tool call:")
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"  - Function: {tool_call.function.name}")
        print(f"    Arguments: {tool_call.function.arguments}")
    
    # Example 3: Multi-turn conversation with tool calls
    print("\nExample 1c: Multi-turn conversation with tool results")
    
    # First, get the tool call request
    messages = [
        {"role": "user", "content": "What's the weather in London and Paris?"}
    ]
    
    response = client.chat.completions.create(
        messages=messages,
        tools=tools,
        model="openai"
    )
    
    # Add the assistant's tool call request to messages
    if response.choices[0].message.tool_calls:
        # Simulate executing the tool and getting results
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content,
            "tool_calls": [tc.to_dict() for tc in response.choices[0].message.tool_calls]
        })
        
        # Add tool results
        for tool_call in response.choices[0].message.tool_calls:
            # Simulate a weather API response
            tool_result = {
                "location": json.loads(tool_call.function.arguments)["location"],
                "temperature": 15,
                "condition": "Partly cloudy"
            }
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })
        
        print("Tool execution complete. Messages in conversation:")
        for i, msg in enumerate(messages):
            print(f"  {i+1}. {msg.get('role', 'N/A')}: {str(msg)[:60]}...")
    
    # ========================================================================
    # Reasoning Examples
    # ========================================================================
    
    print("\n\n2. Using Reasoning:")
    print("-" * SEPARATOR_WIDTH)
    
    # Example 1: Basic reasoning request
    print("\nExample 2a: Request with reasoning_effort")
    print("Note: reasoning_effort parameter may not be supported by all endpoints")
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Solve this math problem: If a train leaves station A at 60 mph and another train leaves station B (100 miles away) at 40 mph, when will they meet?"}
            ],
            reasoning_effort="high",
            model="openai"
        )
        
        if response.choices[0].message.reasoning_content:
            print(f"Reasoning: {response.choices[0].message.reasoning_content[:100]}...")
        else:
            print("Reasoning: Not provided by model")
        print(f"Answer: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error with reasoning_effort parameter: {e}")
        print("The endpoint may not support this parameter. Trying without it...")
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Solve: If a train leaves station A at 60 mph and another train leaves station B (100 miles away) at 40 mph, when will they meet?"}
            ],
            model="openai"
        )
        print(f"Answer: {response.choices[0].message.content}")
    
    # Example 2: Different reasoning levels
    print("\nExample 2b: Testing reasoning_content field (without reasoning_effort)")
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "What is 15 * 24?"}
        ],
        model="openai"
    )
    print(f"  Answer: {response.choices[0].message.content}")
    if response.choices[0].message.reasoning_content:
        print(f"  Reasoning provided: {response.choices[0].message.reasoning_content[:50]}...")
    else:
        print("  Reasoning content: Not provided by this model")
    
    # ========================================================================
    # Streaming with Tool Calls and Reasoning
    # ========================================================================
    
    print("\n\n3. Streaming with Tool Calls and Reasoning:")
    print("-" * SEPARATOR_WIDTH)
    
    print("\nExample 3a: Streaming with tool calls")
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
        tools=tools,
        stream=True,
        model="openai"
    )
    
    print("Streaming response:")
    for chunk in stream:
        if chunk.choices[0].delta.tool_calls:
            print(f"  [Tool call chunk received]")
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
        if chunk.choices[0].finish_reason:
            print(f"\n  Finish reason: {chunk.choices[0].finish_reason}")
    
    print("\n\nExample 3b: Streaming with reasoning_content")
    print("Note: Attempting with reasoning_effort parameter (may not be supported)")
    try:
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": "Calculate the factorial of 5"}],
            reasoning_effort="medium",
            stream=True,
            model="openai"
        )
        
        print("Streaming response with reasoning:")
        reasoning_parts = []
        content_parts = []
        
        for chunk in stream:
            if chunk.choices[0].delta.reasoning_content:
                reasoning_parts.append(chunk.choices[0].delta.reasoning_content)
            if chunk.choices[0].delta.content:
                content_parts.append(chunk.choices[0].delta.content)
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        if reasoning_parts:
            print(f"\n  Reasoning: {''.join(reasoning_parts)[:100]}...")
        else:
            print("\n  No reasoning content in stream")
    except Exception as e:
        print(f"Error: {e}")
        print("Trying without reasoning_effort parameter...")
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": "Calculate the factorial of 5"}],
            stream=True,
            model="openai"
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()
    
    # ========================================================================
    # Combined: Tool Calls + Reasoning
    # ========================================================================
    
    print("\n\n4. Combined Tool Calls and Reasoning:")
    print("-" * SEPARATOR_WIDTH)
    
    print("Note: Attempting with both tools and reasoning_effort (reasoning_effort may not be supported)")
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "I need to know the weather in multiple cities to plan my trip. Check London, Paris, and Berlin."}
            ],
            tools=tools,
            reasoning_effort="medium",
            model="openai"
        )
        
        print("Response with both reasoning and tool calls:")
        if response.choices[0].message.reasoning_content:
            print(f"  Reasoning: {response.choices[0].message.reasoning_content[:80]}...")
        if response.choices[0].message.tool_calls:
            print(f"  Tool calls requested: {len(response.choices[0].message.tool_calls)}")
            for tc in response.choices[0].message.tool_calls:
                print(f"    - {tc.function.name}({tc.function.arguments[:40]}...)")
        if response.choices[0].message.content:
            print(f"  Content: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {e}")
        print("Trying with just tools (no reasoning_effort)...")
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Check weather in London, Paris, and Berlin."}
            ],
            tools=tools,
            model="openai"
        )
        if response.choices[0].message.tool_calls:
            print(f"  Tool calls: {len(response.choices[0].message.tool_calls)}")
        else:
            print(f"  Response: {response.choices[0].message.content}")
    
    print("\n" + "=" * SEPARATOR_WIDTH)
    print("Tool Calls and Reasoning features demonstrated!")
    print("=" * SEPARATOR_WIDTH)


if __name__ == "__main__":
    main()
