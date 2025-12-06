"""
Example script demonstrating text generation with Pollinations.

This script shows various ways to use the text generation API.
"""

from pollinations import Pollinations


def main():
    # Create a client
    client = Pollinations()
    
    print("=" * 60)
    print("Text Generation Examples")
    print("=" * 60)
    
    # Example 1: Simple text generation
    print("\n1. Simple text generation:")
    print("-" * 60)
    response = client.generate_text("What is artificial intelligence?")
    print(response)
    
    # Example 2: With system message
    print("\n2. With system message:")
    print("-" * 60)
    response = client.generate_text(
        "Write a haiku about programming",
        system="You are a creative poetry assistant who writes beautiful haikus"
    )
    print(response)
    
    # Example 3: With temperature control
    print("\n3. Creative response (high temperature):")
    print("-" * 60)
    response = client.generate_text(
        "Tell me a short story about a robot",
        temperature=0.9
    )
    print(response)
    
    # Example 4: Deterministic response with seed
    print("\n4. Deterministic response (with seed):")
    print("-" * 60)
    response1 = client.generate_text("Count to 5", seed=42)
    print(f"First call: {response1}")
    response2 = client.generate_text("Count to 5", seed=42)
    print(f"Second call: {response2}")
    print(f"Same output: {response1 == response2}")
    
    # Example 5: JSON mode
    print("\n5. JSON mode:")
    print("-" * 60)
    response = client.generate_text(
        "Create a JSON object with name, age, and city fields for a fictional person",
        jsonMode=True
    )
    print(response)
    
    # Example 6: Using specific model
    print("\n6. Using specific model:")
    print("-" * 60)
    try:
        response = client.generate_text(
            "Explain quantum entanglement in simple terms",
            model="openai"
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
