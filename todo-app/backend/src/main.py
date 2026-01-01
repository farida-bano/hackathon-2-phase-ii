"""
Evolution of Todo - Phase II Backend API
FastAPI application entry point with environment-aware CORS.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routers import auth_router, todos_router

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Evolution of Todo API",
    description="Phase II - Full-Stack Web Application Backend",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS with environment awareness
def get_allowed_origins():
    """Get allowed origins based on environment."""
    base_origins = [
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Add Vercel preview domain pattern in production
    if settings.is_production:
        return {
            "allowed_origins": base_origins,
            "allow_origin_regex": r"https://.*\.vercel\.app",
        }

    return {"allowed_origins": base_origins}

cors_config = get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.get("allowed_origins", []),
    allow_origin_regex=cors_config.get("allow_origin_regex"),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour
)

# Register routers
app.include_router(auth_router)
app.include_router(todos_router)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower(),
    )
