"""Tests for the EvoForge AI FastAPI application."""

from fastapi.testclient import TestClient

from backend.app.main import app


def test_root_endpoint() -> None:
    """The root endpoint should return application information."""
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "EvoForge AI",
        "version": "0.1.0",
        "status": "operational",
    }


def test_health_endpoint() -> None:
    """The health endpoint should report a healthy service."""
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "evoforge-ai-backend",
    }