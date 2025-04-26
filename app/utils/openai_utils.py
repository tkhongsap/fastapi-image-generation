from typing import Optional
import logging
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)

def get_client() -> Optional[OpenAI]:
    """Get the current OpenAI client instance."""
    # Import here to avoid circular import issues
    from app.utils.openai_client import client as _client
    
    if _client is None:
        logger.error("OpenAI client is None when get_client() was called")
    
    return _client

def get_active_model() -> str:
    """Get the current active image model."""
    # Import here to avoid circular import issues
    from app.utils.openai_client import active_image_model as _active_model
    return _active_model

def is_fallback_mode() -> bool:
    """Check if the client is in fallback mode."""
    # Import here to avoid circular import issues
    from app.utils.openai_client import using_fallback_mode as _fallback_mode
    return _fallback_mode

def reinitialize_client_if_needed() -> bool:
    """Re-initialize the OpenAI client if it's None or in fallback mode."""
    # Import here to avoid circular import issues
    from app.utils import openai_client
    from app.utils.openai_client import initialize_openai_client
    
    if openai_client.client is None or openai_client.using_fallback_mode:
        logger.info("Attempting to reinitialize OpenAI client...")
        try:
            openai_client.client, openai_client.active_image_model, openai_client.using_fallback_mode = initialize_openai_client()
            if openai_client.client is None:
                logger.error("Reinitialization failed: client is still None")
                return False
            else:
                logger.info("OpenAI client reinitialized successfully")
                return True
        except Exception as e:
            logger.error(f"Error during client reinitialization: {e}")
            return False
    return False

def cleanup_client():
    """Clean up the OpenAI client resources."""
    # Import here to avoid circular import issues
    from app.utils import openai_client
    logger.info("Cleaning up OpenAI client resources")
    openai_client.client = None 