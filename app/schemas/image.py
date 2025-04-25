from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any, Dict, Union
from enum import Enum
from app.core.config import ImageModel, ImageSize, ImageQuality, ImageFormat

class GenerateImageRequest(BaseModel):
    """Schema for image generation request."""
    prompt: str = Field(..., description="The text prompt to generate an image from")
    model: ImageModel = Field(default=ImageModel.GPT_IMAGE_1, description="The OpenAI model to use")
    n: int = Field(default=1, ge=1, le=10, description="Number of images to generate")
    size: ImageSize = Field(default=ImageSize.LARGE, description="Size of the generated image")
    quality: ImageQuality = Field(default=ImageQuality.STANDARD, description="Quality of the generated image")
    format: ImageFormat = Field(default=ImageFormat.PNG, description="Format of the generated image")
    background: str = Field(default="auto", description="Background color ('auto', 'transparent', or hex code)")
    
    @validator('background')
    def validate_background(cls, v):
        if v != "auto" and v != "transparent" and not (v.startswith('#') and len(v) in [4, 7]):
            raise ValueError("Background must be 'auto', 'transparent', or a valid hex color code")
        return v

class ImageInfo(BaseModel):
    """Schema for image information in responses."""
    b64_json: Optional[str] = Field(None, description="Base64 encoded image data (if requested)")
    url: Optional[str] = Field(None, description="URL to the image (if URLs were requested)")
    filetype: ImageFormat = Field(..., description="Format of the image")
    size: ImageSize = Field(..., description="Size of the image")

class GenerateImageResponse(BaseModel):
    """Schema for image generation response."""
    created: int = Field(..., description="Unix timestamp of when the images were created")
    model: str = Field(..., description="The model used to generate the images")
    images: List[ImageInfo] = Field(..., description="List of generated images")
    
    class Config:
        schema_extra = {
            "example": {
                "created": 1745575400,
                "model": "gpt-image-1",
                "images": [
                    {
                        "b64_json": "base64_encoded_image_data",
                        "filetype": "png",
                        "size": "1024x1024"
                    }
                ]
            }
        }

class EditImageRequest(BaseModel):
    """Schema for image editing request."""
    prompt: str = Field(..., description="The text prompt describing the edit")
    model: ImageModel = Field(default=ImageModel.DALL_E_2, description="The OpenAI model to use for editing")
    n: int = Field(default=1, ge=1, le=10, description="Number of edit variations to generate")
    size: ImageSize = Field(default=ImageSize.LARGE, description="Size of the edited image")
    format: ImageFormat = Field(default=ImageFormat.PNG, description="Format of the edited image")
    
    # Note: image and mask will be handled as UploadFile in the API endpoint
    # They are not included in this schema

class VariationRequest(BaseModel):
    """Schema for image variation request."""
    model: ImageModel = Field(default=ImageModel.DALL_E_2, description="The OpenAI model to use for variations")
    n: int = Field(default=1, ge=1, le=10, description="Number of variations to generate")
    size: ImageSize = Field(default=ImageSize.LARGE, description="Size of the variation images")
    format: ImageFormat = Field(default=ImageFormat.PNG, description="Format of the variation images")
    
    # Note: image will be handled as UploadFile in the API endpoint
    # It is not included in this schema

class ErrorResponse(BaseModel):
    """Schema for API error responses."""
    error: bool = Field(default=True, description="Indicates this is an error response")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details if available")
    
    class Config:
        schema_extra = {
            "example": {
                "error": True,
                "message": "Invalid request parameters",
                "details": {
                    "prompt": "Field required"
                }
            }
        } 