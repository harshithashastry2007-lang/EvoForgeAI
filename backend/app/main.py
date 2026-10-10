"""EvoForge AI backend application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.ingestion import router as ingestion_router
from backend.app.core.config import get_settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown events."""
    logger.info("application_starting", application=app.title)
    yield
    logger.info("application_stopping", application=app.title)


def create_application() -> FastAPI:
    """Create and securely configure the EvoForge AI application."""
    settings = get_settings()

    application = FastAPI(
        title="EvoForge AI API",
        description=(
            "Backend API for autonomous, self-healing, "
            "and verifiable software engineering."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.debug,
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

    application.include_router(ingestion_router)

    return application



app = create_application()


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Return basic application information."""
    return {
        "name": "EvoForge AI",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Return the current API health status."""
    return {
        "status": "healthy",
        "service": "evoforge-ai-backend",
    }