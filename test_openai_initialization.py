import logging
import base64
import os
import time
from openai import OpenAI
from app.core.config import settings

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gpt_image_1_response():
    """
    Test that the gpt-image-1 model returns base64 data and not URLs
    """
    logger.info("Testing gpt-image-1 response format...")
    
    # Get API key from settings
    API_KEY = settings.OPENAI_API_KEY
    if not API_KEY:
        logger.error("❌ OPENAI_API_KEY is not set or empty.")
        return
    
    try:
        # Create client directly
        client = OpenAI(api_key=API_KEY)
        logger.info("✅ OpenAI client created successfully")
        
        # Generate a test image with minimal parameters
        logger.info("Generating test image with gpt-image-1...")
        start_time = time.time()
        
        response = client.images.generate(
            model="gpt-image-1",
            prompt="A simple test image",
            n=1,
            size="1024x1024"  # Valid sizes for gpt-image-1: 1024x1024, 1024x1536, 1536x1024, auto
        )
        
        duration = time.time() - start_time
        logger.info(f"Request completed in {duration:.2f} seconds")
        
        # Validate response structure
        if not response or not hasattr(response, 'data') or len(response.data) == 0:
            logger.error("❌ No image data in response")
            return
        
        # Check response properties
        image = response.data[0]
        logger.info(f"Response data object type: {type(image)}")
        logger.info(f"Available attributes: {dir(image)}")
        
        # Confirm we have b64_json (required for gpt-image-1)
        if hasattr(image, 'b64_json') and image.b64_json:
            logger.info("✅ Response contains b64_json data as expected")
            b64_sample = image.b64_json[:30] + "..." if len(image.b64_json) > 30 else image.b64_json
            logger.info(f"Base64 data sample: {b64_sample}")
            
            # Validate the base64 data is decodable
            try:
                img_bytes = base64.b64decode(image.b64_json)
                logger.info(f"✅ Base64 data is valid (decoded size: {len(img_bytes)} bytes)")
            except Exception as e:
                logger.error(f"❌ Failed to decode base64 data: {e}")
        else:
            logger.error("❌ Response is missing b64_json data")
        
        # Confirm we do NOT have URL (gpt-image-1 doesn't provide URLs)
        if hasattr(image, 'url') and image.url:
            logger.warning("⚠️ Unexpected URL found in gpt-image-1 response")
            logger.info(f"URL: {image.url}")
        else:
            logger.info("✅ No URL in response, as expected for gpt-image-1")
        
        logger.info("✅ gpt-image-1 response format test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_gpt_image_1_response()