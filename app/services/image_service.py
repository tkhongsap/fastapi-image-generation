"""
Image Generation Service using OpenAI's API

This service handles the communication with OpenAI's API
for image generation, variation, and editing.
"""

import time
import logging
import base64
from typing import Dict, List, Optional, Any, Union

from app.utils.openai_client import (
    get_client, 
    get_active_model, 
    reinitialize_client_if_needed,
    initialize_openai_client
)
from app.schemas.image import (
    ImageGenerationRequest, 
    ImageGenerationResponse,
    ImageData,
    UsageInfo
)
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client on module import
client, active_model, fallback_mode = initialize_openai_client()


async def generate_image(request: ImageGenerationRequest) -> ImageGenerationResponse:
    """
    Generate images using OpenAI's API based on the request parameters.
    
    Args:
        request: The image generation request with prompt, model, etc.
        
    Returns:
        ImageGenerationResponse containing the generated images
        
    Raises:
        Exception: If the OpenAI API call fails
    """
    # Ensure client is initialized
    if reinitialize_client_if_needed():
        logger.info("OpenAI client was reinitialized during the request")
    
    client = get_client()
    if not client:
        raise Exception("OpenAI client could not be initialized")
    
    # Log the generation request
    logger.info(f"Image generation request: model={request.model.value}, prompt={request.prompt[:30]}...")
    
    try:
        # Different API call formats depending on the model
        if request.model.value.startswith("dall-e"):
            # For DALL-E models, use the legacy parameters
            result = client.images.generate(
                model=request.model.value,
                prompt=request.prompt,
                n=request.n,
                size=request.size.value,
                quality=request.quality.value if request.model.value == "dall-e-3" else None,
                response_format="b64_json"
            )
        else:
            # For GPT Image models, use only required parameters
            result = client.images.generate(
                model=request.model.value,
                prompt=request.prompt,
                n=request.n,
                size=request.size.value
            )
        
        # Process results into our response format
        images = []
        for image in result.data:
            images.append(
                ImageData(
                    b64_json=image.b64_json,
                    filetype=request.format.value,
                    size=request.size.value
                )
            )
        
        # Construct usage info if available
        usage = None
        if hasattr(result, 'usage'):
            usage = UsageInfo(
                prompt_tokens=result.usage.prompt_tokens,
                image_tokens=result.usage.total_tokens - result.usage.prompt_tokens,
                total_tokens=result.usage.total_tokens
            )
        
        # Build the response
        response = ImageGenerationResponse(
            id=result.id if hasattr(result, 'id') else f"img_{int(time.time())}",
            created=int(time.time()),
            images=images,
            model=request.model.value,
            usage=usage
        )
        
        logger.info(f"Successfully generated {len(images)} images")
        return response
        
    except Exception as e:
        logger.error(f"Error generating images: {str(e)}")
        raise 