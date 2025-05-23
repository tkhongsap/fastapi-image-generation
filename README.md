# ArtGen FastAPI Service

A web application that generates images using OpenAI's GPT Image and DALL-E models through a FastAPI backend and a clean, modern web interface.

## Features

- Generate images using OpenAI's image models (GPT Image, DALL·E 3, DALL·E 2)
- Configure image size, quality, and format
- Modern, responsive web UI
- RESTful API for programmatic access
- Simple, user-friendly API documentation
- Automatic fallback to DALL-E 3 if GPT Image is not available

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key with access to GPT Image model

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

4. Create a `.env` file in the project root directory with your OpenAI API key:
   ```
   # OpenAI API Configuration
   OPENAI_API_KEY=sk-your-openai-api-key-here
   OPENAI_ORG_ID=org-your-org-id-here-if-applicable

   # API Security Configuration (optional)
   # API_KEY=your-api-key-for-production

   # Application Configuration
   DEBUG=True
   ```

### Running the Application

Start the application with:

```bash
python run.py
```

The application will be available at http://localhost:8000.

For development mode with auto-reload:

```bash
python run.py --reload --debug
```

## API Usage

### Generate Image

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful mountain landscape at sunset",
    "model": "gpt-image-1",
    "n": 1,
    "size": "1024x1024",
    "quality": "medium",
    "format": "png"
  }'
```

## Web Interface

The web interface is accessible at http://localhost:8000/. It provides a user-friendly way to:

1. Enter prompts and generate images
2. Select models, size, and quality
3. Generate multiple images at once
4. Download the generated images

## API Documentation

The API documentation is available at http://localhost:8000/api. It provides:

- Clear endpoint descriptions
- Required and optional parameters
- Parameter types and descriptions
- Response format information

You can also access the raw OpenAPI specification at http://localhost:8000/openapi.json.

## Project Structure

```
fastapi-image-generation/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── generate.py
│   │   │   ├── api.py
│   │   ├── deps.py
│   ├── core/
│   │   ├── config.py
│   ├── schemas/
│   │   ├── image.py
│   ├── services/
│   │   ├── image_service.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── normalize.css
│   │   │   ├── styles.css
│   │   ├── js/
│   │   │   ├── app.js
│   ├── templates/
│   │   ├── index.html
│   │   ├── simple_api.html
│   │   ├── redoc.html
│   ├── utils/
│   │   ├── openai_client.py
│   ├── main.py
├── .env
├── requirements.txt
├── run.py
├── README.md
└── TASKS.md
```

## Notes

- The application includes automatic fallback mechanisms if the GPT Image model is not available, using DALL-E 3 as an alternative.
- In development mode, API key authentication is disabled for easier testing.

## License

MIT 

## Environment Variables & Security

This project uses [python-dotenv](https://pypi.org/project/python-dotenv/) to manage environment variables securely. **Never commit your `.env` file or secrets to version control.**

- The `.env` file is listed in `.gitignore` and will not be tracked by git.
- You must create your own `.env` file in the project root (see Setup section above).
- Required variables (e.g., `OPENAI_API_KEY`) are validated at startup. The app will not run if they are missing or invalid.
- For different environments (development, test, production), use separate `.env` files as needed (e.g., `.env.dev`, `.env.prod`).

**Troubleshooting:**
If you see errors about missing or invalid environment variables, ensure your `.env` file exists and contains all required keys. Refer to the example in the Setup section. 