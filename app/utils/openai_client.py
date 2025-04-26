"""
OpenAI Client Initialization Utility

This module handles the initialization and management of the OpenAI client,
including API key validation, model selection, and error handling.
"""

import os
import logging
from typing import Optional, Tuple
from pathlib import Path
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
    """
    Initialize and validate the OpenAI client with proper error handling.
    
    Returns:
        Tuple containing:
        - OpenAI client (or None if initialization failed)
        - Active image model being used
        - Boolean indicating if we're in fallback mode (always False now)
    """
    global client, active_image_model, using_fallback_mode
    
    API_KEY = settings.OPENAI_API_KEY
    ORG_ID = os.getenv("OPENAI_ORG_ID")

    if not API_KEY:
        logger.error("❌ OPENAI_API_KEY is not set or empty.")
        using_fallback_mode = True
        return None, active_image_model, True

    key_preview = f"{API_KEY[:7]}........{API_KEY[-4:]}" if len(API_KEY) > 11 else "***masked***"
    is_project_based_key = API_KEY.startswith("sk-proj-")
    logger.info(f"OpenAI API key detected: {key_preview} ({'project-based' if is_project_based_key else 'standard'})")

    try:
        client = OpenAI(
            api_key=API_KEY,
            organization=ORG_ID,  # Will be None if not set
            default_headers={"OpenAI-Beta": "assistants=v1"}
        )

        # Test API key with a simple call
        logger.info(f"Attempting to validate API key and check model: {IMAGE_MODEL}")
        # For gpt-image-1, make a test image generation call
        try:
            _ = client.images.generate(
                model=IMAGE_MODEL,
                prompt="test",
                n=1,
                size="1024x1024"
            )
        except Exception as test_exc:
            logger.error(f"❌ Failed to validate gpt-image-1 via image generation endpoint: {test_exc}")
            raise test_exc
        logger.info(f"✅ OpenAI API key validated successfully. Using image model: {IMAGE_MODEL}")
        active_image_model = IMAGE_MODEL
        using_fallback_mode = False

    except AuthenticationError as e:
        logger.error(f"❌ AUTHENTICATION ERROR: Invalid OpenAI API key or insufficient permissions. Status: {e.status_code}. Message: {e.message}")
        if is_project_based_key:
            logger.error("Project-based keys (sk-proj-*) may have limited permissions. Check model access in your OpenAI project settings.")
        else:
            logger.error("Verify your API key at https://platform.openai.com/account/api-keys")
        client = None
        using_fallback_mode = True
    except APIStatusError as e:
        logger.error(f"❌ API ERROR during validation: Status {e.status_code}. Message: {e.message}")
        client = None
        using_fallback_mode = True
    except APIConnectionError as e:
        logger.error(f"❌ CONNECTION ERROR: Could not connect to OpenAI API. {e}")
        client = None
        using_fallback_mode = True
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred during OpenAI client initialization: {e}")
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