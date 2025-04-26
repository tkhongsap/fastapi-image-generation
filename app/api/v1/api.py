"""
API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import generate

# Create API router for v1
api_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

# Include all endpoint routers
api_router.include_router(
    generate.router,
    prefix="/generate",
    tags=["image-generation"],
) 