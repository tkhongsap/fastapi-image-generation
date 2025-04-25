from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

from app.core.config import settings
from app.api.routes import api_router

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Path("logs/app.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A lightweight service for AI image generation using OpenAI API",
    version="0.1.0",
    debug=settings.DEBUG
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Root route redirects to UI
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Admin dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    # In a real app, check for admin authorization here
    return templates.TemplateResponse("dashboard.html", {"request": request})

# API documentation
@app.get("/docs/api", response_class=HTMLResponse)
async def api_docs(request: Request):
    with open("app/static/docs/api.md", "r") as f:
        api_md_content = f.read()
    return templates.TemplateResponse("api_docs.html", {"request": request, "api_content": api_md_content})

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG) 