from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import os
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings.
    Values will be loaded from environment variables or .env file
    """
    # API settings
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "ArtGen FastAPI Service"
    PROJECT_DESCRIPTION: str = "A FastAPI service for image generation using OpenAI models"
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False)
    
    # OpenAI API settings
    OPENAI_API_KEY: Optional[str] = None
    
    # Image Generation Settings
    DEFAULT_MODEL: str = "gpt-image-1"
    DEFAULT_SIZE: str = "1024x1024"
    DEFAULT_QUALITY: str = "medium"
    DEFAULT_FORMAT: str = "png"
    
    # API security
    # (For MVP, we'll use API key in header, later implement Auth0/SSO)
    API_KEY_NAME: str = "x-api-key"
    API_KEY: Optional[str] = None
    
    # Define settings for loading from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env file
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings to avoid reloading from env each time
    """
    return Settings()


settings = get_settings() 