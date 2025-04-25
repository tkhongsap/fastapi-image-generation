import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from enum import Enum

# Load environment variables from .env file if it exists
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Try to load from env.example for development
    example_env_path = Path('.') / 'env.example'
    if example_env_path.exists():
        load_dotenv(dotenv_path=example_env_path)
        print("Warning: Using env.example for configuration. This should only be used in development.")

# Environment
class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

# Logging levels
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
    def __str__(self):
        return self.value

# OpenAI Image Models
class ImageModel(str, Enum):
    GPT_IMAGE_1 = "gpt-image-1"
    DALL_E_3 = "dall-e-3"
    DALL_E_2 = "dall-e-2"

# Image sizes
class ImageSize(str, Enum):
    SMALL = "256x256"
    MEDIUM = "512x512"
    LARGE = "1024x1024"
    SQUARE_HD = "1792x1792"
    WIDE = "1792x1024"
    TALL = "1024x1792"

# Image quality
class ImageQuality(str, Enum):
    STANDARD = "standard"
    HD = "hd"

# Image format
class ImageFormat(str, Enum):
    PNG = "png"
    WEBP = "webp"

# Settings class
class Settings:
    # App settings
    APP_NAME: str = os.getenv("APP_NAME", "ArtGen FastAPI Service")
    ENV: Environment = os.getenv("ENV", Environment.DEVELOPMENT)
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Security settings
    AUTH_ENABLED: bool = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "20").split("#")[0].strip())
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "3600").split("#")[0].strip())
    
    # Validate settings
    def validate(self):
        if self.ENV == Environment.PRODUCTION:
            assert self.OPENAI_API_KEY, "OPENAI_API_KEY must be set in production"
            assert self.SECRET_KEY, "SECRET_KEY must be set in production"
        
        if not self.OPENAI_API_KEY and self.ENV != Environment.TESTING:
            logging.warning("OPENAI_API_KEY not set. API calls will fail.")

# Create settings instance
settings = Settings()

# Validate in non-testing environments
if settings.ENV != Environment.TESTING:
    settings.validate() 