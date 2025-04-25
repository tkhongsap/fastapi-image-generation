from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging
import json
from typing import Optional
import base64
from io import BytesIO

from app.core.config import ImageModel, ImageSize, ImageQuality, ImageFormat
from app.schemas.image import (
    GenerateImageRequest, 
    GenerateImageResponse, 
    EditImageRequest, 
    VariationRequest,
    ErrorResponse
)
from app.services.openai_service import OpenAIService

# Set up logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Factory function for OpenAI service
def get_openai_service():
    return OpenAIService()

@router.post(
    "/generate",
    response_model=GenerateImageResponse,
    responses={
        200: {"model": GenerateImageResponse},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Generate image from text prompt"
)
async def generate_image(
    request: GenerateImageRequest,
    background_tasks: BackgroundTasks,
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    Generate an image using OpenAI's image generation models.
    
    - **prompt**: Text description of the desired image
    - **model**: OpenAI model to use (gpt-image-1, dall-e-3, dall-e-2)
    - **n**: Number of images to generate (1-10)
    - **size**: Size of the generated image (256x256, 512x512, 1024x1024, etc.)
    - **quality**: Quality of the generated image (standard, hd)
    - **format**: Format of the generated image (png, webp)
    - **background**: Background color (auto, transparent, or hex color code)
    """
    try:
        # Generate image via OpenAI service
        response = await openai_service.generate_image(
            prompt=request.prompt,
            model=request.model,
            n=request.n,
            size=request.size,
            quality=request.quality,
            response_format=request.format,
            background=request.background
        )
        
        # Log successful request
        background_tasks.add_task(
            logger.info,
            f"Generated {request.n} image(s) with model {request.model} for prompt: '{request.prompt[:30]}...'"
        )
        
        return response
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail={"error": True, "message": "Invalid request parameters", "details": json.loads(e.json())}
        )
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": True, "message": f"Failed to generate image: {str(e)}"}
        )

@router.post(
    "/edit",
    response_model=GenerateImageResponse,
    responses={
        200: {"model": GenerateImageResponse},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Edit an existing image"
)
async def edit_image(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    mask: Optional[UploadFile] = File(None),
    model: ImageModel = Form(ImageModel.DALL_E_2),
    n: int = Form(1),
    size: ImageSize = Form(ImageSize.LARGE),
    format: ImageFormat = Form(ImageFormat.PNG),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    Edit an existing image using OpenAI's image editing models.
    
    - **prompt**: Text description of the desired edit
    - **image**: Image file to edit
    - **mask**: Optional mask file (transparent areas will be edited)
    - **model**: OpenAI model to use (dall-e-2 only currently supported)
    - **n**: Number of edits to generate (1-10)
    - **size**: Size of the edited image
    - **format**: Format of the edited image (png, webp)
    """
    try:
        # Validate request
        if model != ImageModel.DALL_E_2:
            logger.warning(f"Requested model {model} does not support edits, using DALL-E-2 instead")
            model = ImageModel.DALL_E_2
        
        # Read image file
        image_bytes = await image.read()
        
        # Read mask file if provided
        mask_bytes = None
        if mask:
            mask_bytes = await mask.read()
        
        # Create edit request
        edit_request = EditImageRequest(
            prompt=prompt,
            model=model,
            n=n,
            size=size,
            format=format
        )
        
        # Call OpenAI service
        response = await openai_service.edit_image(
            image=image_bytes,
            prompt=edit_request.prompt,
            mask=mask_bytes,
            model=edit_request.model,
            n=edit_request.n,
            size=edit_request.size,
            response_format=edit_request.format
        )
        
        # Log successful request
        background_tasks.add_task(
            logger.info,
            f"Edited image with model {edit_request.model} for prompt: '{edit_request.prompt[:30]}...'"
        )
        
        return response
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail={"error": True, "message": "Invalid request parameters", "details": json.loads(e.json())}
        )
    except Exception as e:
        logger.error(f"Error editing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": True, "message": f"Failed to edit image: {str(e)}"}
        )

@router.post(
    "/variation",
    response_model=GenerateImageResponse,
    responses={
        200: {"model": GenerateImageResponse},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Create variations of an existing image"
)
async def create_variation(
    image: UploadFile = File(...),
    model: ImageModel = Form(ImageModel.DALL_E_2),
    n: int = Form(1),
    size: ImageSize = Form(ImageSize.LARGE),
    format: ImageFormat = Form(ImageFormat.PNG),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    Create variations of an existing image using OpenAI's image variation models.
    
    - **image**: Image file to create variations of
    - **model**: OpenAI model to use (dall-e-2 only currently supported)
    - **n**: Number of variations to generate (1-10)
    - **size**: Size of the variation images
    - **format**: Format of the variation images (png, webp)
    """
    try:
        # Validate request
        if model != ImageModel.DALL_E_2:
            logger.warning(f"Requested model {model} does not support variations, using DALL-E-2 instead")
            model = ImageModel.DALL_E_2
        
        # Read image file
        image_bytes = await image.read()
        
        # Create variation request
        variation_request = VariationRequest(
            model=model,
            n=n,
            size=size,
            format=format
        )
        
        # Call OpenAI service
        response = await openai_service.create_variation(
            image=image_bytes,
            model=variation_request.model,
            n=variation_request.n,
            size=variation_request.size,
            response_format=variation_request.format
        )
        
        # Log successful request
        background_tasks.add_task(
            logger.info,
            f"Created {variation_request.n} variation(s) of image with model {variation_request.model}"
        )
        
        return response
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail={"error": True, "message": "Invalid request parameters", "details": json.loads(e.json())}
        )
    except Exception as e:
        logger.error(f"Error creating image variations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": True, "message": f"Failed to create image variations: {str(e)}"}
        ) 