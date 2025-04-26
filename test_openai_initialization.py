import logging
import base64
from app.utils.openai_client import initialize_openai_client, get_client, get_active_model

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai():
    # Test 1: Initialize OpenAI client
    logger.info("Testing OpenAI client initialization...")
    client, active_model, fallback_mode = initialize_openai_client()
    
    if client is None:
        logger.error("❌ OpenAI client initialization failed")
        return
    logger.info(f"✅ OpenAI client initialization successful - Using model: {active_model}")
    
    # Test 2: Generate a simple image
    logger.info("Testing image generation...")
    try:
        response = client.images.generate(
            model=get_active_model(),
            prompt="A cute baby sea otter",
            n=1,
            size="1024x1024"
        )
        
        if response and response.data and len(response.data) > 0:
            image_data = response.data[0]
            
            # Check if URL is available
            if hasattr(image_data, 'url') and image_data.url:
                logger.info(f"✅ Image generated successfully with URL: {image_data.url}")
            else:
                logger.info(f"Image generated but no URL available")
            
            logger.info("✅ Image generation test passed")
        else:
            logger.error("❌ No image data received")
    except Exception as e:
        logger.error(f"❌ Image generation failed: {e}")

if __name__ == "__main__":
    test_openai()