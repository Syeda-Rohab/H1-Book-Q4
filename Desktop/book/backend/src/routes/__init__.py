"""API routes for textbook content generation backend.

This package contains FastAPI route handlers for:
- Health checks
- Content generation
- Chapter CRUD operations
"""

from .health_routes import router as health_router

__all__ = ["health_router"]
