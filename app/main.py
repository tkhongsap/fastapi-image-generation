"""
Main FastAPI application entry point
"""

import logging
import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.api import api_router
from app.core.config import settings
from app.utils.openai_client import initialize_openai_client

# Load environment variables from .env at the very top
try:
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
        print(f"Loaded environment variables from {dotenv_path}")
    else:
        print("Warning: .env file not found. Environment variables may be missing.")
except Exception as dotenv_exc:
    print(f"Error loading .env file: {dotenv_exc}")

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client, model, fallback = initialize_openai_client()
if fallback:
    logger.warning("⚠️ Running in fallback mode! OpenAI API client initialization failed.")

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be limited to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Root endpoint - serve the UI
@app.get("/", include_in_schema=False)
async def root(request: Request):
    """Serve the web UI"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": settings.PROJECT_NAME}
    )

# Health check endpoint
@app.get("/health", include_in_schema=False)
async def health():
    """Health check endpoint"""
    return {"status": "ok", "api_version": settings.VERSION}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup: log the configuration and initialize components"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"OpenAI client status: {'Fallback Mode' if fallback else 'OK'}")
    logger.info(f"Active image model: {model}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown: perform cleanup"""
    logger.info(f"Shutting down {settings.PROJECT_NAME}")
    from app.utils.openai_client import cleanup_client
    cleanup_client() 