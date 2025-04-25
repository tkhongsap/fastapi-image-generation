"""
API dependencies and security helpers
"""

from fastapi import Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings

# API key security scheme
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Validate the API key from the request header
    
    This is a simple security measure for the MVP. In a production environment,
    this would be replaced with a more robust auth system like OAuth or JWT.
    
    Returns:
        str: The validated API key
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    # If API key security is not enabled, allow all requests
    if not settings.API_KEY:
        return "no_key_required"
        
    if api_key_header and api_key_header == settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"}
        ) 