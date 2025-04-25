"""
API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import generate

# Create API router for v1
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(generate.router, prefix="/generate", tags=["image-generation"]) 