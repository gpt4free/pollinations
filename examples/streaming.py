"""
Example demonstrating streaming support for text generation.

This script shows how to use streaming with both the OpenAI-compatible
API and the native API.
"""

from polinations import Polinations


def main():
    print("=" * 70)
    print("Streaming Examples")
    print("=" * 70)
    
    # Initialize client
    client = Polinations()
    
    # ========================================================================
    # OpenAI-Compatible Streaming API
    # ========================================================================
    
    print("\n1. Basic Streaming (OpenAI-compatible):")
    print("-" * 70)
    
    stream = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Count to 10"}
        ],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")
    
    print("\n2. Streaming with System Message:")
    print("-" * 70)
    
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a creative poet."},
            {"role": "user", "content": "Write a haiku about coding"}
        ],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")
    
    print("\n3. Streaming with Temperature Control:")
    print("-" * 70)
    
    stream = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Tell me a very short story about a robot"}
        ],
        temperature=0.9,
        stream=True
    )
    
    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_response += delta
            print(delta, end="", flush=True)
        
        # Check finish reason
        if chunk.choices[0].finish_reason:
            print(f"\n\n[Finished: {chunk.choices[0].finish_reason}]")
    
    print(f"\n[Full response length: {len(full_response)} characters]")
    
    print("\n4. Collecting Chunks for Analysis:")
    print("-" * 70)
    
    stream = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "List 5 programming languages"}
        ],
        stream=True
    )
    
    chunks = []
    for chunk in stream:
        chunks.append(chunk)
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print(f"\n\n[Received {len(chunks)} chunks]")
    
    # ========================================================================
    # Native API Streaming
    # ========================================================================
    
    print("\n5. Native API Streaming:")
    print("-" * 70)
    
    stream = client.generate_text_stream(
        "What is Python?",
        model="openai"
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")
    
    print("\n6. Native API with System Message:")
    print("-" * 70)
    
    stream = client.generate_text_stream(
        "Write a short joke",
        system="You are a friendly comedian",
        temperature=0.8
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")
    
    # ========================================================================
    # Advanced Use Cases
    # ========================================================================
    
    print("\n7. Real-time Processing:")
    print("-" * 70)
    print("Simulating character-by-character display:")
    
    import time
    
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say 'Hello World'"}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            # Simulate processing delay
            time.sleep(0.05)
    
    print("\n")
    
    print("\n" + "=" * 70)
    print("Streaming examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
