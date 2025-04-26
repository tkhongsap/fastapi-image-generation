import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"OPENAI_API_KEY loaded: {api_key[:10]}.......................{api_key[-10:]}")
else:
    print("OPENAI_API_KEY not found in environment!")

try:
    client = OpenAI(api_key=api_key)
    prompt = """
    A children's book drawing of a veterinarian using a stethoscope to 
    listen to the heartbeat of a baby otter.
    """
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt
    )
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    with open("otter.png", "wb") as f:
        f.write(image_bytes)
    print("Image generated and saved as otter.png")
except Exception as e:
    print(f"Error during OpenAI API call: {e}") 