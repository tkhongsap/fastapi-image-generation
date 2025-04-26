"""
Main FastAPI application entry point
"""

import logging
import os
import markdown
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from app.api.v1.api import api_router
from app.core.config import settings
from app.utils.openai_client import initialize_openai_client
from app.utils.openai_utils import cleanup_client

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
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
    openapi_version="3.0.2",
    openapi_tags=[{
        "name": "image-generation",
        "description": "Endpoints for generating images using OpenAI models"
    }]
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

# API Documentation with Swagger UI
@app.get("/docs", include_in_schema=False)
async def swagger_ui(request: Request):
    """Serve custom Swagger UI"""
    return templates.TemplateResponse(
        "api.html", 
        {
            "request": request, 
            "title": f"API Documentation | {settings.PROJECT_NAME}",
            "active_doc": "swagger",
            "doc_url": "/swagger-ui"
        }
    )

# API Documentation with ReDoc
@app.get("/api", include_in_schema=False)
async def redoc_ui(request: Request):
    """Serve simple API documentation instead of ReDoc"""
    return templates.TemplateResponse(
        "simple_api.html", 
        {
            "request": request, 
            "title": f"API Reference | {settings.PROJECT_NAME}"
        }
    )

# Raw Swagger UI
@app.get("/swagger-ui", include_in_schema=False)
async def swagger_ui_html(request: Request):
    """Serve raw Swagger UI HTML"""
    return templates.TemplateResponse(
        "swagger.html", 
        {
            "request": request,
            "title": f"{settings.PROJECT_NAME} - API Documentation",
            "openapi_url": "/openapi.json"
        }
    )

# Raw ReDoc UI
@app.get("/redoc", include_in_schema=False)
async def redoc_ui_html(request: Request):
    """Serve raw ReDoc HTML"""
    # Simple implementation to avoid loading issues
    return templates.TemplateResponse(
        "redoc.html", 
        {
            "request": request,
            "title": f"{settings.PROJECT_NAME} - API Reference",
            "openapi_url": "/openapi.json",
            "redoc_js_url": "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
        }
    )

# Simple API Documentation (no ReDoc)
@app.get("/simple-api", include_in_schema=False)
async def simple_api_docs(request: Request):
    """Serve a simple, custom API documentation page without ReDoc"""
    return templates.TemplateResponse(
        "simple_api.html", 
        {
            "request": request,
            "title": f"Simple API Reference | {settings.PROJECT_NAME}"
        }
    )

# Help page endpoint
@app.get("/help", response_class=HTMLResponse, include_in_schema=False)
async def help_page(request: Request):
    """Serve the help page"""
    try:
        help_md_path = Path("docs/help.md")
        if not help_md_path.exists():
            logger.error(f"Help markdown file not found at {help_md_path}")
            return templates.TemplateResponse(
                "help.html", 
                {
                    "request": request, 
                    "title": f"Help | {settings.PROJECT_NAME}",
                    "content": "<h1>Help Content Unavailable</h1><p>The help documentation is currently unavailable. Please try again later.</p>"
                }
            )
        
        md_content = help_md_path.read_text(encoding="utf-8")
        html_content = markdown.markdown(
            md_content, 
            extensions=['fenced_code', 'tables', 'toc']
        )
        
        return templates.TemplateResponse(
            "help.html", 
            {
                "request": request, 
                "title": f"Help | {settings.PROJECT_NAME}",
                "content": html_content
            }
        )
    except Exception as e:
        logger.error(f"Error rendering help page: {str(e)}")
        return templates.TemplateResponse(
            "help.html", 
            {
                "request": request, 
                "title": f"Help | {settings.PROJECT_NAME}",
                "content": f"<h1>Error Loading Help</h1><p>An error occurred while loading the help content: {str(e)}</p>"
            }
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
    cleanup_client() 