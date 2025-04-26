from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum


class ImageModels(str, Enum):
    """Available image generation models"""
    GPT_IMAGE = "gpt-image-1"
    DALLE_3 = "dall-e-3"
    DALLE_2 = "dall-e-2"


class ImageSizes(str, Enum):
    """Available image sizes"""
    SMALL = "256x256"  # Only for DALL-E 2
    MEDIUM = "512x512"  # Only for DALL-E 2
    LARGE = "1024x1024"  # Valid for all models
    PORTRAIT = "1024x1536"  # Valid for DALL-E 3 and GPT-Image-1
    LANDSCAPE = "1536x1024"  # Valid for DALL-E 3 and GPT-Image-1
    AUTO = "auto"  # Only for GPT-Image-1


class ImageQualities(str, Enum):
    """Available image qualities"""
    STANDARD = "standard"
    HD = "hd"  # Only for DALL-E 3
    MEDIUM = "medium" # For GPT Image


class ImageFormats(str, Enum):
    """Available image formats"""
    PNG = "png"
    JPEG = "jpeg"


class ImageGenerationRequest(BaseModel):
    """
    Request schema for image generation
    """
    model: ImageModels = Field(default=ImageModels.GPT_IMAGE, description="The model to use for generation")
    prompt: str = Field(..., min_length=1, max_length=4000, description="The text prompt to generate an image from")
    n: int = Field(default=1, ge=1, le=10, description="The number of images to generate")
    size: ImageSizes = Field(default=ImageSizes.LARGE, description="The size of the generated image")
    quality: ImageQualities = Field(default=ImageQualities.MEDIUM, description="The quality of the generated image")
    format: ImageFormats = Field(default=ImageFormats.PNG, description="The format to return the image in")
    background: Literal["auto", "transparent"] = Field(default="auto", description="Whether to make the background transparent")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "model": "gpt-image-1",
                "prompt": "A castle on a cliff at dawn",
                "size": "1024x1024",
                "quality": "medium",
                "format": "png"
            }
        }
    }


class ImageData(BaseModel):
    """Individual image data in the response"""
    b64_json: str = Field(..., description="Base64-encoded image data")
    filetype: str = Field(..., description="File type of the generated image")
    size: str = Field(..., description="Size of the generated image")


class UsageInfo(BaseModel):
    """Token usage information"""
    prompt_tokens: int
    image_tokens: int
    total_tokens: int


class ImageGenerationResponse(BaseModel):
    """
    Response schema for image generation
    """
    id: str = Field(..., description="Unique identifier for the generation request")
    created: int = Field(..., description="Unix timestamp for when the generation was created")
    images: List[ImageData] = Field(..., description="List of generated images")
    model: str = Field(..., description="The model used for generation")
    usage: Optional[UsageInfo] = Field(None, description="Token usage information") 