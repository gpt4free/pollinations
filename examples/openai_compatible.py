"""
Example demonstrating OpenAI-compatible API usage.

This script shows how to use the OpenAI-compatible interface for both
chat completions and image generation.
"""

from polinations import Polinations


def main():
    print("=" * 70)
    print("OpenAI-Compatible API Examples")
    print("=" * 70)
    
    # Initialize client (with or without API key)
    # Without API key (uses free public API)
    client = Polinations()
    
    # With API key (uses enter.pollinations.ai or gen.pollinations.ai)
    # client = Polinations(api_key="your-api-key-here")
    
    # ========================================================================
    # Chat Completions API (OpenAI-compatible)
    # ========================================================================
    
    print("\n1. Simple Chat Completion:")
    print("-" * 70)
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "What is Python?"}
        ]
    )
    print(f"Response: {response.choices[0].message.content}")
    
    print("\n2. Chat with System Message:")
    print("-" * 70)
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Explain list comprehension in Python"}
        ],
        model="openai"
    )
    print(f"Response: {response.choices[0].message.content}")
    
    print("\n3. Chat with Temperature Control:")
    print("-" * 70)
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Write a creative story about a robot"}
        ],
        temperature=0.9,
        max_tokens=200
    )
    print(f"Response: {response.choices[0].message.content}")
    
    print("\n4. Accessing Response Fields:")
    print("-" * 70)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="openai"
    )
    print(f"Object Type: {response.object}")
    print(f"Model: {response.model}")
    print(f"Finish Reason: {response.choices[0].finish_reason}")
    print(f"Message Role: {response.choices[0].message.role}")
    print(f"Message Content: {response.choices[0].message.content}")
    
    # ========================================================================
    # Images API (OpenAI-compatible)
    # ========================================================================
    
    print("\n5. Simple Image Generation:")
    print("-" * 70)
    response = client.images.generate(
        prompt="A serene mountain landscape at sunset"
    )
    print(f"Image URL: {response.data[0]['url']}")
    
    print("\n6. Image with Size:")
    print("-" * 70)
    response = client.images.generate(
        prompt="A futuristic city skyline",
        size="1024x768"
    )
    print(f"Image URL: {response.data[0]['url'][:80]}...")
    
    print("\n7. Image with Model:")
    print("-" * 70)
    response = client.images.generate(
        prompt="Abstract art with vibrant colors",
        model="flux",
        size="512x512"
    )
    print(f"Image URL: {response.data[0]['url'][:80]}...")
    print(f"Revised Prompt: {response.data[0]['revised_prompt']}")
    
    # ========================================================================
    # Comparison with Native API
    # ========================================================================
    
    print("\n8. Comparison: OpenAI-compatible vs Native API:")
    print("-" * 70)
    
    # OpenAI-compatible
    openai_response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}]
    )
    openai_text = openai_response.choices[0].message.content
    
    # Native API
    native_text = client.generate_text("Hello")
    
    print(f"OpenAI-compatible: {openai_text[:50]}...")
    print(f"Native API: {native_text[:50]}...")
    print("\nBoth methods access the same underlying API!")
    
    print("\n" + "=" * 70)
    print("OpenAI-compatible API works perfectly!")
    print("=" * 70)


if __name__ == "__main__":
    main()
