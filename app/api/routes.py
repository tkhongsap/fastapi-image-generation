from fastapi import APIRouter
from app.api.v1 import image_generation

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(image_generation.router, prefix="/v1", tags=["image-generation"]) 