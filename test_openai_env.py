import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY not found in environment!")
    exit(1)

# Print masked API key for verification
masked_key = f"{api_key[:7]}...{api_key[-4:]}" if len(api_key) > 11 else "***masked***"
print(f"Using API key: {masked_key}")

# Initialize client
client = OpenAI(api_key=api_key)

# Generate image
try:
    print("Generating image...")
    response = client.images.generate(
        model="gpt-image-1",
        prompt="A cute baby sea otter",
        n=1,
        size="1024x1024"
    )
    
    # Save the image (if URL is available)
    if hasattr(response.data[0], 'url'):
        print(f"Image URL: {response.data[0].url}")
        print("✅ Image generation successful!")
    else:
        print("Image generated but no URL available")
    
except Exception as e:
    print(f"❌ Error during image generation: {e}") 