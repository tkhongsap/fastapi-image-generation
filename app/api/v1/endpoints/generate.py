"""
Image generation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.image import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_service import generate_image
from app.api.deps import get_api_key

# Create router
router = APIRouter()


@router.post("/", response_model=ImageGenerationResponse, status_code=200)
async def create_image(
    request: ImageGenerationRequest,
    api_key: str = Depends(get_api_key)
) -> ImageGenerationResponse:
    """
    Generate an image based on the provided prompt and parameters.
    
    - **model**: The model to use for image generation (gpt-image-1, dall-e-3, dall-e-2)
    - **prompt**: The text prompt to generate an image from
    - **n**: Number of images to generate (1-10)
    - **size**: Size of the generated image
    - **quality**: Quality of the generated image
    - **format**: Format to return the image in (png, jpeg)
    """
    try:
        return await generate_image(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )


# Add OpenAPI documentation code samples
create_image.openapi_extra = {
    "x-codeSamples": [
        {
            "lang": "curl",
            "source": """
curl -X 'POST' \\
  'https://artgen-api.example.com/api/v1/generate/' \\
  -H 'accept: application/json' \\
  -H 'x-api-key: YOUR_API_KEY' \\
  -H 'Content-Type: application/json' \\
  -d '{
  "model": "gpt-image-1",
  "prompt": "A castle on a cliff at dawn",
  "n": 1,
  "size": "1024x1024",
  "quality": "medium",
  "format": "png"
}'
"""
        },
        {
            "lang": "python",
            "source": """
import requests
import json

url = "https://artgen-api.example.com/api/v1/generate/"
headers = {
    "accept": "application/json",
    "x-api-key": "YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-image-1",
    "prompt": "A castle on a cliff at dawn",
    "n": 1,
    "size": "1024x1024",
    "quality": "medium",
    "format": "png"
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2))
"""
        },
        {
            "lang": "javascript",
            "source": """
const options = {
  method: 'POST',
  headers: {
    'accept': 'application/json',
    'x-api-key': 'YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-image-1',
    prompt: 'A castle on a cliff at dawn',
    n: 1,
    size: '1024x1024',
    quality: 'medium',
    format: 'png'
  })
};

fetch('https://artgen-api.example.com/api/v1/generate/', options)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
"""
        }
    ]
} 