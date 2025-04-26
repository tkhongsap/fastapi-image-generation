"""
OpenAI Client Initialization Utility

This module handles the initialization and management of the OpenAI client,
including API key validation, model selection, and error handling.
"""

import os
import logging
from typing import Optional, Tuple
from openai import OpenAI, OpenAIError, APIStatusError, APIConnectionError, AuthenticationError
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Model selection
IMAGE_MODEL = "gpt-image-1"

# Global client variable and state tracking
client: Optional[OpenAI] = None
active_image_model = IMAGE_MODEL
using_fallback_mode = False

def initialize_openai_client() -> Tuple[Optional[OpenAI], str, bool]:
    """Initialize and validate the OpenAI client."""
    global client, active_image_model, using_fallback_mode

    api_key = settings.OPENAI_API_KEY
    org_id = os.getenv("OPENAI_ORG_ID")
    if not api_key:
        logger.error("OPENAI_API_KEY is not set.")
        using_fallback_mode = True
        return None, active_image_model, True

    logger.info(f"OpenAI API key detected: {api_key[:7]}...{api_key[-7:] if len(api_key) > 11 else ''}")
    try:
        client = OpenAI(api_key=api_key, organization=org_id, default_headers={"OpenAI-Beta": "assistants=v1"})
        models = client.models.list()
        if IMAGE_MODEL not in [m.id for m in models.data]:
            logger.error(f"Model {IMAGE_MODEL} not available for this API key.")
            using_fallback_mode = True
            return None, active_image_model, True
        logger.info(f"OpenAI API key validated. Using model: {IMAGE_MODEL}")
        active_image_model = IMAGE_MODEL
        using_fallback_mode = False
    except (AuthenticationError, APIStatusError, APIConnectionError, Exception) as e:
        logger.error(f"OpenAI client initialization failed: {e}")
        client = None
        using_fallback_mode = True

    return client, active_image_model, using_fallback_mode

def get_client() -> Optional[OpenAI]:
    """
    Get the current OpenAI client instance.
    
    Returns:
        The OpenAI client or None if not initialized
    """
    return client

def get_active_model() -> str:
    """
    Get the current active image model.
    
    Returns:
        The active image model name
    """
    return active_image_model

def is_fallback_mode() -> bool:
    """
    Check if the client is in fallback mode.
    
    Returns:
        True if in fallback mode, False otherwise
    """
    return using_fallback_mode

def reinitialize_client_if_needed() -> bool:
    """
    Re-initialize the OpenAI client if it's None or in fallback mode.
    
    Returns:
        True if reinitialization was attempted, False otherwise
    """
    global client, using_fallback_mode, active_image_model
    
    if client is None or using_fallback_mode:
        logger.info("Attempting to reinitialize OpenAI client...")
        client, active_image_model, using_fallback_mode = initialize_openai_client()
        return True
    return False

def cleanup_client():
    """Clean up the OpenAI client resources"""
    global client
    # Note: OpenAI client doesn't have a close/cleanup method as of now
    # but we can set it to None to help with garbage collection
    client = None 