# ArtGen FastAPI Service

A lightweight service that exposes OpenAI's Image API through a FastAPI backend and a minimalist web frontend.

## Features

- Generate images using OpenAI's image models (GPT Image, DALL·E 3, DALL·E 2)
- Edit existing images with prompts and masks
- Create variations of images
- Configure image size, quality, format, and other parameters
- Simple and intuitive web interface
- RESTful API for programmatic access

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-image-generation.git
   cd fastapi-image-generation
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory based on `env.example`:
   ```
   # OpenAI API configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # Application settings
   APP_NAME=ArtGen FastAPI Service
   ENV=development  # Options: development, testing, production
   DEBUG=true
   LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

   # Security settings
   AUTH_ENABLED=false
   SECRET_KEY=your_secure_random_secret_key_here

   # Rate limiting
   RATE_LIMIT_ENABLED=true
   RATE_LIMIT_REQUESTS=20  # Number of requests allowed
   RATE_LIMIT_PERIOD=3600  # Period in seconds (1 hour)
   ```

### Running the Application

Start the application with:

```bash
python run.py
```

The application will be available at http://localhost:8000.

## API Usage

### Generate Image

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful mountain landscape at sunset",
    "model": "gpt-image-1",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "format": "png",
    "background": "auto"
  }'
```

### Edit Image

```bash
curl -X POST "http://localhost:8000/api/v1/edit" \
  -F "prompt=Add a castle on the mountain" \
  -F "image=@path/to/image.png" \
  -F "mask=@path/to/mask.png" \
  -F "model=dall-e-2" \
  -F "n=1" \
  -F "size=1024x1024" \
  -F "format=png"
```

### Create Variation

```bash
curl -X POST "http://localhost:8000/api/v1/variation" \
  -F "image=@path/to/image.png" \
  -F "model=dall-e-2" \
  -F "n=1" \
  -F "size=1024x1024" \
  -F "format=png"
```

## Web Interface

The web interface is accessible at http://localhost:8000/. It provides a user-friendly way to:

1. Enter prompts and generate images
2. Upload and edit existing images
3. Create variations of images
4. Configure all image generation parameters
5. Download or copy the generated images

## Project Structure

```
fastapi-image-generation/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── image_generation.py
│   │   ├── routes.py
│   ├── core/
│   │   ├── config.py
│   ├── schemas/
│   │   ├── image.py
│   ├── services/
│   │   ├── openai_service.py
│   ├── static/
│   ├── templates/
│   │   ├── index.html
│   ├── main.py
├── logs/
├── .env
├── env.example
├── requirements.txt
├── run.py
├── README.md
└── TASKS.md
```

## License

MIT 