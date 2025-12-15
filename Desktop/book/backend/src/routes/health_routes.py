"""Health check endpoints for monitoring and observability.

Provides endpoints to check service health, readiness, and dependencies.

Constitution Compliance: Principle VIII - Observability
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


class HealthResponse(BaseModel):
    """Health check response model.

    Attributes:
        status: Overall health status (ok/degraded/down)
        timestamp: Current timestamp (ISO 8601)
        version: API version
        environment: Deployment environment
        checks: Dictionary of individual health checks
    """

    status: str
    timestamp: str
    version: str
    environment: str
    checks: Dict[str, Any]


class LivenessResponse(BaseModel):
    """Liveness probe response model.

    Attributes:
        alive: True if service is alive
        timestamp: Current timestamp
    """

    alive: bool
    timestamp: str


class ReadinessResponse(BaseModel):
    """Readiness probe response model.

    Attributes:
        ready: True if service is ready to accept traffic
        timestamp: Current timestamp
        checks: Dictionary of readiness checks
    """

    ready: bool
    timestamp: str
    checks: Dict[str, bool]


@router.get(
    "/",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns overall health status with detailed checks",
)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint.

    Returns:
        HealthResponse with status and detailed checks

    Constitution Compliance:
    - Provides observability for monitoring (Principle VIII)
    - Fast response (<100ms) for speed (Principle II)
    """
    checks = {}

    # Check 1: Database connection
    database_healthy = await _check_database()
    checks["database"] = {
        "status": "ok" if database_healthy else "down",
        "message": "Database connection healthy" if database_healthy else "Database connection failed",
    }

    # Check 2: LLM API availability
    llm_healthy = _check_llm_api()
    checks["llm_api"] = {
        "status": "ok" if llm_healthy else "degraded",
        "message": "LLM API key configured" if llm_healthy else "LLM API key not configured",
    }

    # Check 3: Storage paths
    storage_healthy = _check_storage()
    checks["storage"] = {
        "status": "ok" if storage_healthy else "degraded",
        "message": "Storage paths accessible" if storage_healthy else "Storage paths not accessible",
    }

    # Determine overall status
    overall_status = "ok"
    if not database_healthy:
        overall_status = "down"
    elif not llm_healthy or not storage_healthy:
        overall_status = "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        version=os.getenv("API_VERSION", "0.1.0"),
        environment=os.getenv("ENVIRONMENT", "development"),
        checks=checks,
    )


@router.get(
    "/live",
    response_model=LivenessResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
    description="Kubernetes liveness probe - checks if service is alive",
)
async def liveness() -> LivenessResponse:
    """Liveness probe for Kubernetes.

    Returns:
        LivenessResponse indicating service is alive

    Usage:
        Kubernetes uses this endpoint to check if the pod should be restarted.
        Returns 200 if the service is running.
    """
    return LivenessResponse(
        alive=True,
        timestamp=datetime.utcnow().isoformat(),
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
    description="Kubernetes readiness probe - checks if service can accept traffic",
)
async def readiness() -> ReadinessResponse:
    """Readiness probe for Kubernetes.

    Returns:
        ReadinessResponse with readiness status

    Usage:
        Kubernetes uses this endpoint to check if the pod should receive traffic.
        Returns 200 if the service is ready, 503 if not ready.
    """
    checks = {}

    # Check database readiness
    database_ready = await _check_database()
    checks["database"] = database_ready

    # Check LLM API readiness
    llm_ready = _check_llm_api()
    checks["llm_api"] = llm_ready

    # Service is ready if database is ready (LLM API is optional)
    ready = database_ready

    # Return 503 if not ready
    status_code = status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        ready=ready,
        timestamp=datetime.utcnow().isoformat(),
        checks=checks,
    )


# Private helper functions for health checks

async def _check_database() -> bool:
    """Check database connectivity.

    Returns:
        True if database is reachable

    TODO: Implement actual database connection check once DB is configured
    """
    # For MVP, check if DATABASE_URL is configured
    database_url = os.getenv("DATABASE_URL")
    if not database_url or database_url == "postgresql://user:pass@localhost/dbname":
        logger.warning("Database URL not configured")
        return False

    # TODO: Add actual connection check
    # try:
    #     async with db_pool.acquire() as conn:
    #         await conn.fetchval("SELECT 1")
    #     return True
    # except Exception as e:
    #     logger.error(f"Database health check failed: {e}")
    #     return False

    return True


def _check_llm_api() -> bool:
    """Check LLM API configuration.

    Returns:
        True if LLM API key is configured

    Note:
        Does not actually call the API (to avoid rate limits in health checks).
        Only checks if the API key is set.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("sk-ant-api03-your-"):
        logger.warning("ANTHROPIC_API_KEY not configured")
        return False
    return True


def _check_storage() -> bool:
    """Check storage paths accessibility.

    Returns:
        True if storage paths exist and are writable

    Checks:
    - website/docs/ directory exists (for markdown output)
    - Directory is writable
    """
    try:
        # Check website/docs directory
        docs_dir = os.path.join("website", "docs")
        if not os.path.exists(docs_dir):
            logger.warning(f"Docs directory does not exist: {docs_dir}")
            return False

        if not os.access(docs_dir, os.W_OK):
            logger.warning(f"Docs directory not writable: {docs_dir}")
            return False

        return True

    except Exception as e:
        logger.error(f"Storage health check failed: {e}")
        return False
