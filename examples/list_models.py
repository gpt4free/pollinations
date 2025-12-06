"""
Example script to list available models from Polinations.

This script demonstrates how to retrieve the list of available models
for both text and image generation.
"""

from polinations import Polinations
import json


def main():
    # Create a client
    client = Polinations()
    
    print("=" * 60)
    print("Polinations Available Models")
    print("=" * 60)
    
    # Get image models
    print("\n1. Image Generation Models:")
    print("-" * 60)
    try:
        image_models = client.get_image_models()
        print(f"Total image models: {len(image_models)}")
        print("\nAvailable models:")
        for i, model in enumerate(image_models, 1):
            print(f"  {i}. {model}")
    except Exception as e:
        print(f"Error fetching image models: {e}")
    
    # Get text models
    print("\n2. Text Generation Models:")
    print("-" * 60)
    try:
        text_models = client.get_text_models()
        print(f"Total text models: {len(text_models)}")
        print("\nAvailable models:")
        for i, model in enumerate(text_models, 1):
            if isinstance(model, dict):
                print(f"  {i}. {json.dumps(model, indent=4)}")
            else:
                print(f"  {i}. {model}")
    except Exception as e:
        print(f"Error fetching text models: {e}")
    
    # Cache demonstration
    print("\n3. Cache Demonstration:")
    print("-" * 60)
    print("Fetching image models again (should use cache)...")
    image_models_cached = client.get_image_models()
    print(f"Models from cache: {len(image_models_cached)}")
    
    print("\nForce refreshing cache...")
    image_models_fresh = client.get_image_models(force_refresh=True)
    print(f"Fresh models: {len(image_models_fresh)}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
