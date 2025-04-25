"""
Run script for the ArtGen FastAPI Image Generation Service

This script starts the FastAPI application using uvicorn.
"""

import uvicorn
import logging
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("run")

def create_directories():
    """Create necessary directories if they don't exist"""
    dirs = [
        "app/static/css",
        "app/static/js",
        "app/templates",
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the ArtGen FastAPI service")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Ensure directories exist
    create_directories()
    
    # Set debug mode from arguments or environment
    debug_mode = args.debug or os.getenv("DEBUG", "False").lower() in ("true", "1", "t", "yes")
    
    # Log startup information
    logger.info(f"Starting ArtGen FastAPI service on {args.host}:{args.port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    # Start the server
    uvicorn.run(
        "app.main:app", 
        host=args.host, 
        port=args.port, 
        reload=args.reload,
        log_level="debug" if debug_mode else "info",
    ) 