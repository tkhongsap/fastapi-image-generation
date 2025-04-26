from typing import Optional
from openai import OpenAI
from app.utils.openai_client import (
    client as _client,
    active_image_model as _active_image_model,
    using_fallback_mode as _using_fallback_mode,
    initialize_openai_client
)
import logging

logger = logging.getLogger(__name__)

def get_client() -> Optional[OpenAI]:
    """Get the current OpenAI client instance."""
    return _client

def get_active_model() -> str:
    """Get the current active image model."""
    return _active_image_model

def is_fallback_mode() -> bool:
    """Check if the client is in fallback mode."""
    return _using_fallback_mode

def reinitialize_client_if_needed() -> bool:
    """Re-initialize the OpenAI client if it's None or in fallback mode."""
    from app.utils import openai_client
    if openai_client.client is None or openai_client.using_fallback_mode:
        logger.info("Attempting to reinitialize OpenAI client...")
        openai_client.client, openai_client.active_image_model, openai_client.using_fallback_mode = initialize_openai_client()
        return True
    return False

def cleanup_client():
    """Clean up the OpenAI client resources."""
    from app.utils import openai_client
    openai_client.client = None 