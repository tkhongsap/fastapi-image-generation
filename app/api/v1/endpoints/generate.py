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