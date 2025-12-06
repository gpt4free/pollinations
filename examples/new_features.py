"""
Example script demonstrating new image generation features.

This script shows the new parameters available in the API.
"""

from pollinations import Pollinations


def main():
    client = Pollinations()
    
    print("=" * 60)
    print("New Image Generation Features")
    print("=" * 60)
    
    # Example 1: Negative prompt
    print("\n1. Using negative_prompt to avoid unwanted elements:")
    print("-" * 60)
    url = client.generate_image(
        "a beautiful portrait",
        negative_prompt="blur, distorted, low quality",
        width=512,
        height=512
    )
    print(f"URL: {url}")
    
    # Example 2: Quality control
    print("\n2. Using quality parameter:")
    print("-" * 60)
    url = client.generate_image(
        "a mountain landscape",
        quality="high",
        width=1024,
        height=768
    )
    print(f"URL: {url}")
    
    # Example 3: Transparent background
    print("\n3. Generate with transparent background:")
    print("-" * 60)
    url = client.generate_image(
        "a red apple on a plate",
        transparent=True,
        width=512,
        height=512
    )
    print(f"URL: {url}")
    
    # Example 4: Guidance scale
    print("\n4. Control how closely to follow the prompt:")
    print("-" * 60)
    url = client.generate_image(
        "an abstract painting",
        guidance_scale=10.0,
        width=768,
        height=768
    )
    print(f"URL: {url}")
    
    # Example 5: Safety filters
    print("\n5. Enable safety filters:")
    print("-" * 60)
    url = client.generate_image(
        "a peaceful garden scene",
        safe=True,
        width=1024,
        height=1024
    )
    print(f"URL: {url}")
    
    # Example 6: Image-to-image
    print("\n6. Reference image for image-to-image generation:")
    print("-" * 60)
    reference_url = "https://image.pollinations.ai/prompt/a%20cat"
    url = client.generate_image(
        "a cat wearing a hat",
        image=reference_url,
        width=512,
        height=512
    )
    print(f"URL: {url}")
    
    # Example 7: Combining multiple parameters
    print("\n7. Combining multiple new parameters:")
    print("-" * 60)
    url = client.generate_image(
        "a professional headshot",
        negative_prompt="blur, distorted, overexposed",
        quality="hd",
        guidance_scale=7.5,
        safe=True,
        enhance=True,
        width=1024,
        height=1024
    )
    print(f"URL: {url}")
    
    print(f"\n{'=' * 60}")
    print("All examples completed!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
