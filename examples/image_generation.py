"""
Example script demonstrating image generation with Polinations.

This script shows various ways to use the image generation API.
"""

import os
from polinations import Polinations


def main():
    # Create a client
    client = Polinations()
    
    print("=" * 60)
    print("Image Generation Examples")
    print("=" * 60)
    
    # Create output directory for images
    output_dir = "generated_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Example 1: Simple image generation (URL only)
    print("\n1. Simple image generation (URL):")
    print("-" * 60)
    image_url = client.generate_image("A beautiful sunset over mountains")
    print(f"Image URL: {image_url}")
    
    # Example 2: Generate with specific dimensions
    print("\n2. Generate with specific dimensions:")
    print("-" * 60)
    image_url = client.generate_image(
        "A futuristic city at night with neon lights",
        width=1024,
        height=768
    )
    print(f"Image URL: {image_url}")
    
    # Example 3: Generate with specific model
    print("\n3. Generate with specific model:")
    print("-" * 60)
    try:
        # First, let's see available models
        models = client.get_image_models()
        print(f"Available models: {', '.join(models[:5])}...")  # Show first 5
        
        # Use a specific model
        if models:
            model = models[0]
            image_url = client.generate_image(
                "A portrait of a wise old wizard",
                model=model
            )
            print(f"Using model '{model}'")
            print(f"Image URL: {image_url}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Download image to file
    print("\n4. Download image to file:")
    print("-" * 60)
    output_path = os.path.join(output_dir, "downloaded_image.png")
    client.download_image(
        "A cute cat wearing sunglasses sitting on a beach",
        output_path,
        width=512,
        height=512
    )
    print(f"Image saved to: {output_path}")
    
    # Example 5: Generate with seed for reproducibility
    print("\n5. Generate with seed (reproducible):")
    print("-" * 60)
    url1 = client.generate_image("A red sports car", seed=12345)
    url2 = client.generate_image("A red sports car", seed=12345)
    print(f"URL 1: {url1}")
    print(f"URL 2: {url2}")
    print(f"URLs are same: {url1 == url2}")
    
    # Example 6: Enhanced prompt
    print("\n6. Enhanced prompt:")
    print("-" * 60)
    image_url = client.generate_image(
        "forest",
        enhance=True,
        width=768,
        height=768
    )
    print(f"Image URL with enhanced prompt: {image_url}")
    
    # Example 7: Private image (not published to feed)
    print("\n7. Private image:")
    print("-" * 60)
    image_url = client.generate_image(
        "A secret garden with magical flowers",
        private=True
    )
    print(f"Private image URL: {image_url}")
    
    # Example 8: No logo
    print("\n8. Image without Polinations logo:")
    print("-" * 60)
    image_url = client.generate_image(
        "A minimalist logo design",
        nologo=True
    )
    print(f"Image URL (no logo): {image_url}")
    
    print(f"\n{'=' * 60}")
    print(f"All examples completed!")
    print(f"Check the '{output_dir}' directory for downloaded images.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
