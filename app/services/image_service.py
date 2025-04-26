"""
Image Generation Service using OpenAI's API

This service handles the communication with OpenAI's API
for image generation, variation, and editing.
"""

import time
import logging
import base64
from typing import Dict, List, Optional, Any, Union

from app.utils.openai_utils import (
    get_client, 
    get_active_model, 
    reinitialize_client_if_needed,
    cleanup_client
)
from app.schemas.image import (
    ImageGenerationRequest, 
    ImageGenerationResponse,
    ImageData,
    UsageInfo,
    ImageModels
)
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Note: We no longer initialize the client here.
# The client is initialized in app/utils/openai_client.py which happens during application startup


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
    # Always attempt to reinitialize if needed
    reinitialize_client_if_needed()
    
    # Get the client (should never be None now)
    client = get_client()
    if not client:
        logger.error("Critical error: OpenAI client is None even after reinitialization")
        raise Exception("OpenAI client could not be initialized. Check API key and network connection.")
    
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
                response_format="b64_json"  # Always request base64 data for consistent handling
            )
        else:
            # For GPT Image models, which always return base64 data
            # Note: response_format is not supported for gpt-image-1
            result = client.images.generate(
                model=request.model.value,
                prompt=request.prompt,
                n=request.n,
                size=request.size.value
            )
        
        # Process results into our response format
        images = []
        for image in result.data:
            # For gpt-image-1, we should always have b64_json
            if request.model.value == ImageModels.GPT_IMAGE.value and hasattr(image, 'b64_json'):
                images.append(
                    ImageData(
                        b64_json=image.b64_json,
                        filetype=request.format.value,
                        size=request.size.value
                    )
                )
            # For DALL-E models with b64_json response format
            elif hasattr(image, 'b64_json') and image.b64_json:
                images.append(
                    ImageData(
                        b64_json=image.b64_json,
                        filetype=request.format.value,
                        size=request.size.value
                    )
                )
            # Fallback for URL responses (should not happen with our configuration)
            elif hasattr(image, 'url') and image.url:
                logger.warning(f"Unexpected URL response for model {request.model.value}")
                # We would need to download the image from URL and convert to base64
                # This branch should not be reached with our current configuration
                raise Exception(f"URL response format not supported for {request.model.value}")
            else:
                logger.error(f"Invalid response format from OpenAI API for model {request.model.value}")
                raise Exception("Image data missing from API response")
        
        # Construct usage info if available
        usage = None
        if hasattr(result, 'usage'):
            # Check if usage has prompt_tokens or if it's a dictionary
            if isinstance(result.usage, dict):
                # GPT-image-1 might return a different format
                usage = UsageInfo(
                    prompt_tokens=result.usage.get('prompt_tokens', 0),
                    image_tokens=result.usage.get('total_tokens', 0) - result.usage.get('prompt_tokens', 0),
                    total_tokens=result.usage.get('total_tokens', 0)
                )
            else:
                # Standard format with prompt_tokens as attributes
                try:
                    usage = UsageInfo(
                        prompt_tokens=result.usage.prompt_tokens,
                        image_tokens=result.usage.total_tokens - result.usage.prompt_tokens,
                        total_tokens=result.usage.total_tokens
                    )
                except AttributeError:
                    # If any attributes are missing, log and continue without usage info
                    logger.warning(f"Incomplete usage information in response: {result.usage}")
                    usage = None
        
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