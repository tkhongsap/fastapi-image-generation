import logging
import base64
from typing import List, Optional, Dict, Any, Union
from openai import OpenAI, AsyncOpenAI
from openai.types.images_response import ImagesResponse
import asyncio
import httpx
from app.core.config import settings, ImageModel, ImageSize, ImageQuality, ImageFormat

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service to handle interactions with OpenAI API for image generation."""
    
    def __init__(self):
        """Initialize the OpenAI client with API key from settings."""
        self.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.async_client = AsyncOpenAI(api_key=self.api_key)
        
        # Log initialization (without API key)
        logger.info(f"OpenAI service initialized with API key: {'set' if self.api_key else 'not set'}")
    
    async def generate_image(
        self,
        prompt: str,
        model: ImageModel = ImageModel.GPT_IMAGE_1,
        n: int = 1,
        size: ImageSize = ImageSize.LARGE,
        quality: ImageQuality = ImageQuality.STANDARD,
        response_format: ImageFormat = ImageFormat.PNG,
        background: str = "auto",
    ) -> Dict[str, Any]:
        """
        Generate image(s) based on a text prompt using OpenAI API.
        
        Args:
            prompt: Text description of the desired image
            model: OpenAI model to use for image generation
            n: Number of images to generate (1-10)
            size: Size of the generated image
            quality: Quality of the generated image (standard or hd)
            response_format: Format of the generated image (png or webp)
            background: Background color (auto, transparent, or hex color)
            
        Returns:
            Dictionary containing generated image data and metadata
        """
        try:
            logger.info(f"Generating image with prompt: '{prompt[:50]}...' using model: {model}")
            
            # Validate n is within limits
            n = max(1, min(n, 10))
            
            # Build request parameters
            params = {
                "model": model.value,
                "prompt": prompt,
                "n": n,
                "size": size.value,
                "quality": quality.value,
                "response_format": response_format.value,
            }
            
            # Only include background if specified for DALL-E-3 or GPT-Image
            if model != ImageModel.DALL_E_2 and background != "auto":
                params["background"] = background
            
            # Make API call with retries
            response = await self._with_retries(
                lambda: self.async_client.images.generate(**params)
            )
            
            # Process response
            result = {
                "model": model.value,
                "images": [],
                "created": response.created,
            }
            
            # Extract images from response
            for image_data in response.data:
                image_info = {
                    "filetype": response_format.value,
                    "size": size.value,
                }
                
                if hasattr(image_data, 'b64_json') and image_data.b64_json:
                    image_info["b64_json"] = image_data.b64_json
                elif hasattr(image_data, 'url') and image_data.url:
                    image_info["url"] = image_data.url
                
                result["images"].append(image_info)
            
            # Log success
            logger.info(f"Successfully generated {n} image(s) with model {model}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise
    
    async def edit_image(
        self,
        image: bytes,
        prompt: str,
        mask: Optional[bytes] = None,
        model: ImageModel = ImageModel.DALL_E_2,  # Only DALL-E-2 currently supports edit
        n: int = 1,
        size: ImageSize = ImageSize.LARGE,
        response_format: ImageFormat = ImageFormat.PNG,
    ) -> Dict[str, Any]:
        """
        Edit an existing image based on a text prompt and optional mask.
        
        Args:
            image: The image to edit in bytes format
            prompt: Text description of the desired edit
            mask: Optional mask specifying which areas to edit (transparent areas will be edited)
            model: OpenAI model to use (currently only DALL-E-2 supports edit)
            n: Number of edits to generate (1-10)
            size: Size of the edited image
            response_format: Format of the generated image (png or webp)
            
        Returns:
            Dictionary containing edited image data and metadata
        """
        try:
            logger.info(f"Editing image with prompt: '{prompt[:50]}...' using model: {model}")
            
            # DALL-E-2 is the only model that supports edits at the moment
            if model != ImageModel.DALL_E_2:
                logger.warning(f"Model {model} does not support image editing, using DALL-E-2 instead")
                model = ImageModel.DALL_E_2
            
            # Validate n is within limits
            n = max(1, min(n, 10))
            
            # Prepare parameters for the API call
            params = {
                "model": model.value,
                "image": image,
                "prompt": prompt,
                "n": n,
                "size": size.value,
                "response_format": response_format.value,
            }
            
            # Add mask if provided
            if mask:
                params["mask"] = mask
            
            # Make the API call with retries
            response = await self._with_retries(
                lambda: self.async_client.images.edits.create(**params)
            )
            
            # Process the response
            result = {
                "model": model.value,
                "images": [],
                "created": response.created,
            }
            
            # Extract images from response
            for image_data in response.data:
                image_info = {
                    "filetype": response_format.value,
                    "size": size.value,
                }
                
                if hasattr(image_data, 'b64_json') and image_data.b64_json:
                    image_info["b64_json"] = image_data.b64_json
                elif hasattr(image_data, 'url') and image_data.url:
                    image_info["url"] = image_data.url
                
                result["images"].append(image_info)
            
            # Log success
            logger.info(f"Successfully edited image with {n} variation(s)")
            return result
            
        except Exception as e:
            logger.error(f"Error editing image: {str(e)}")
            raise
    
    async def create_variation(
        self,
        image: bytes,
        model: ImageModel = ImageModel.DALL_E_2,  # Only DALL-E-2 currently supports variations
        n: int = 1,
        size: ImageSize = ImageSize.LARGE,
        response_format: ImageFormat = ImageFormat.PNG,
    ) -> Dict[str, Any]:
        """
        Create variations of an existing image.
        
        Args:
            image: The image to create variations of in bytes format
            model: OpenAI model to use (currently only DALL-E-2 supports variations)
            n: Number of variations to generate (1-10)
            size: Size of the variation images
            response_format: Format of the generated images (png or webp)
            
        Returns:
            Dictionary containing variation image data and metadata
        """
        try:
            logger.info(f"Creating variations of image using model: {model}")
            
            # DALL-E-2 is the only model that supports variations at the moment
            if model != ImageModel.DALL_E_2:
                logger.warning(f"Model {model} does not support variations, using DALL-E-2 instead")
                model = ImageModel.DALL_E_2
            
            # Validate n is within limits
            n = max(1, min(n, 10))
            
            # Prepare parameters for the API call
            params = {
                "model": model.value,
                "image": image,
                "n": n,
                "size": size.value,
                "response_format": response_format.value,
            }
            
            # Make the API call with retries
            response = await self._with_retries(
                lambda: self.async_client.images.variations.create(**params)
            )
            
            # Process the response
            result = {
                "model": model.value,
                "images": [],
                "created": response.created,
            }
            
            # Extract images from response
            for image_data in response.data:
                image_info = {
                    "filetype": response_format.value,
                    "size": size.value,
                }
                
                if hasattr(image_data, 'b64_json') and image_data.b64_json:
                    image_info["b64_json"] = image_data.b64_json
                elif hasattr(image_data, 'url') and image_data.url:
                    image_info["url"] = image_data.url
                
                result["images"].append(image_info)
            
            # Log success
            logger.info(f"Successfully created {n} variation(s) of the image")
            return result
            
        except Exception as e:
            logger.error(f"Error creating image variations: {str(e)}")
            raise
    
    async def _with_retries(self, func, max_retries=3, base_delay=1):
        """
        Execute a function with exponential backoff retries.
        
        Args:
            func: The async function to execute
            max_retries: Maximum number of retries before giving up
            base_delay: Base delay between retries (will be exponentially increased)
            
        Returns:
            The result of the function if successful
            
        Raises:
            The last exception encountered if all retries fail
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return await func()
            except (httpx.HTTPError, asyncio.TimeoutError) as e:
                last_exception = e
                
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Request failed: {str(e)}. Retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Request failed after {max_retries} retries: {str(e)}")
                    raise
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise
                
        if last_exception:
            raise last_exception 