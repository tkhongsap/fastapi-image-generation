import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from enum import Enum

# Set up logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
env_path = Path('.') / '.env'
logger.debug(f"Checking for .env file at: {env_path.absolute()}")
if env_path.exists():
    logger.info(f"Loading environment from .env file: {env_path.absolute()}")
    load_dotenv(dotenv_path=env_path)
else:
    # Try to load from env.example for development
    example_env_path = Path('.') / 'env.example'
    logger.debug(f"No .env file found, checking for env.example at: {example_env_path.absolute()}")
    if example_env_path.exists():
        logger.warning(f"Loading environment from env.example: {example_env_path.absolute()}")
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
        logger.debug("Validating settings...")
        if self.ENV == Environment.PRODUCTION:
            assert self.OPENAI_API_KEY, "OPENAI_API_KEY must be set in production"
            assert self.SECRET_KEY, "SECRET_KEY must be set in production"
        
        # Check API key
        if not self.OPENAI_API_KEY:
            logging.warning("OPENAI_API_KEY not set. API calls will fail.")
        else:
            # Log a preview of the API key for debugging (masking most of it)
            key_preview = f"{self.OPENAI_API_KEY[:7]}...{self.OPENAI_API_KEY[-4:]}" if len(self.OPENAI_API_KEY) > 11 else "(too short)"
            logger.debug(f"OPENAI_API_KEY loaded: {key_preview}")
            
            # Check for multi-line API key which could cause issues
            if '\n' in self.OPENAI_API_KEY:
                logger.critical("OPENAI_API_KEY contains newline characters! This will cause authentication failures.")
            
            if len(self.OPENAI_API_KEY) < 20:
                logger.warning("OPENAI_API_KEY is suspiciously short. This may cause issues.")
            
        logger.debug("Settings validation completed")

# Create settings instance
logger.debug("Creating settings instance...")
settings = Settings()

# Validate in non-testing environments
if settings.ENV != Environment.TESTING:
    logger.debug("Running settings validation...")
    settings.validate() 
    logger.debug("Settings initialization completed") 