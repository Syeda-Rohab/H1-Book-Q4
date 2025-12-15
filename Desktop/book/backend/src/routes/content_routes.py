"""API routes for textbook content generation.

Provides REST endpoints for triggering generation, checking status,
and retrieving chapter content.

Based on tasks.md: T027-T030 - Content generation API endpoints
"""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.services.generation_service import GenerationService
from backend.src.services.chapter_service import ChapterService
from backend.src.models.chapter import ChapterStatus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/content",
    tags=["content"],
)


# Dependency to get database session
# Note: This is a placeholder - actual implementation depends on app setup
async def get_db_session() -> AsyncSession:
    """Get async database session.

    This is a placeholder. In production, this would be implemented
    using FastAPI's dependency injection system with a session factory.

    Yields:
        AsyncSession
    """
    # TODO: Implement actual database session factory
    # Example:
    # async with async_session_factory() as session:
    #     yield session
    raise NotImplementedError("Database session factory not implemented yet")


# Request/Response models

class GenerationRequest(BaseModel):
    """Request body for starting batch generation."""

    include_extended: bool = Field(
        default=False,
        description="Include P2/P3 chapters (default: False for MVP - 6 chapters)",
    )
    model_override: Optional[str] = Field(
        default=None,
        description="Optional model override (e.g., 'claude-3-5-sonnet-20241022')",
    )


class GenerationResponse(BaseModel):
    """Response for starting batch generation."""

    job_id: str = Field(description="UUID of the generation job")
    message: str = Field(description="Success message")
    chapters_total: int = Field(description="Total chapters to be generated")


class JobStatusResponse(BaseModel):
    """Response for job status query."""

    job_id: str
    status: str = Field(description="Job status (pending/in_progress/completed/failed)")
    progress: dict = Field(description="Progress information")
    started_at: str
    completed_at: Optional[str]
    token_usage: int
    model_used: str
    errors: List[dict]
    is_complete: bool


class ChapterMetadata(BaseModel):
    """Chapter metadata for list responses."""

    id: str
    chapter_number: int
    title: str
    slug: str
    word_count: int
    reading_time_minutes: int
    status: str
    created_at: str
    updated_at: str


class ChapterDetail(BaseModel):
    """Detailed chapter information."""

    id: str
    chapter_number: int
    title: str
    slug: str
    word_count: int
    reading_time_minutes: int
    status: str
    validation_errors: List[dict]
    created_at: str
    updated_at: str
    content_path: Optional[str] = None
    docusaurus_url: Optional[str] = None


class ChaptersListResponse(BaseModel):
    """Response for listing all chapters."""

    total: int
    chapters: List[ChapterMetadata]


# API Endpoints

@router.post(
    "/generate",
    response_model=GenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start batch chapter generation",
    description=(
        "Triggers batch generation of all textbook chapters. "
        "Generation runs asynchronously in the background. "
        "Use the returned job_id to check progress via /generation-status/{job_id}."
    ),
)
async def start_generation(
    request: GenerationRequest,
    db: AsyncSession = Depends(get_db_session),
) -> GenerationResponse:
    """Start batch generation for all chapters (T027).

    Args:
        request: Generation configuration
        db: Database session

    Returns:
        GenerationResponse with job_id

    Raises:
        HTTPException: If generation fails to start
    """
    try:
        logger.info(
            f"Starting generation (extended={request.include_extended}, "
            f"model={request.model_override})"
        )

        service = GenerationService(db)
        job_id = await service.start_batch_generation(
            include_extended=request.include_extended,
            model_override=request.model_override,
        )

        chapters_total = 8 if request.include_extended else 6

        return GenerationResponse(
            job_id=str(job_id),
            message="Generation started successfully",
            chapters_total=chapters_total,
        )

    except Exception as e:
        logger.error(f"Failed to start generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start generation: {str(e)}",
        )


@router.get(
    "/generation-status/{job_id}",
    response_model=JobStatusResponse,
    summary="Get generation job status",
    description=(
        "Check the status and progress of a generation job. "
        "Returns progress percentage, token usage, and any errors."
    ),
)
async def get_generation_status(
    job_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> JobStatusResponse:
    """Get the status of a generation job (T028).

    Args:
        job_id: Generation job UUID
        db: Database session

    Returns:
        JobStatusResponse with progress and status

    Raises:
        HTTPException: If job not found
    """
    try:
        logger.info(f"Getting status for job {job_id}")

        service = GenerationService(db)
        job_status = await service.get_job_status(job_id)

        if not job_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Generation job {job_id} not found",
            )

        return JobStatusResponse(**job_status)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get job status: {str(e)}",
        )


@router.get(
    "/chapters",
    response_model=ChaptersListResponse,
    summary="List all chapters",
    description=(
        "Get a list of all chapters with metadata (number, title, word count, status). "
        "Optionally filter by status."
    ),
)
async def list_chapters(
    status_filter: Optional[str] = Query(
        None,
        description="Filter by status (pending/generated/validated/published/failed)",
    ),
    db: AsyncSession = Depends(get_db_session),
) -> ChaptersListResponse:
    """List all chapters with optional status filter (T029).

    Args:
        status_filter: Optional status to filter by
        db: Database session

    Returns:
        ChaptersListResponse with chapter list

    Raises:
        HTTPException: If status_filter is invalid or query fails
    """
    try:
        logger.info(f"Listing chapters (status_filter={status_filter})")

        service = ChapterService(db)

        if status_filter:
            # Validate status
            try:
                status_enum = ChapterStatus(status_filter)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status: {status_filter}. Valid values: {[s.value for s in ChapterStatus]}",
                )

            chapters = await service.list_chapters_by_status(status_enum)
        else:
            chapters = await service.list_all_chapters()

        # Convert to response model
        chapter_metadata = [
            ChapterMetadata(
                id=str(ch.id),
                chapter_number=ch.chapter_number,
                title=ch.title,
                slug=ch.slug,
                word_count=ch.word_count,
                reading_time_minutes=ch.reading_time_minutes,
                status=ch.status.value,
                created_at=ch.created_at.isoformat(),
                updated_at=ch.updated_at.isoformat(),
            )
            for ch in chapters
        ]

        return ChaptersListResponse(
            total=len(chapter_metadata),
            chapters=chapter_metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to list chapters: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list chapters: {str(e)}",
        )


@router.get(
    "/chapters/{chapter_number}",
    response_model=ChapterDetail,
    summary="Get chapter details",
    description=(
        "Get detailed information about a specific chapter by its number (1-8). "
        "Includes validation errors and content file paths."
    ),
)
async def get_chapter(
    chapter_number: int = Query(
        ...,
        ge=1,
        le=8,
        description="Chapter number (1-8)",
    ),
    db: AsyncSession = Depends(get_db_session),
) -> ChapterDetail:
    """Get detailed chapter information by chapter number (T030).

    Args:
        chapter_number: Chapter number (1-8)
        db: Database session

    Returns:
        ChapterDetail with full chapter information

    Raises:
        HTTPException: If chapter not found
    """
    try:
        logger.info(f"Getting details for chapter {chapter_number}")

        service = ChapterService(db)
        chapter = await service.get_chapter_by_number(chapter_number)

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter {chapter_number} not found",
            )

        # Extract content paths if available
        content_path = None
        docusaurus_url = None
        if chapter.content:
            content_path = chapter.content.markdown_path
            docusaurus_url = chapter.content.docusaurus_url

        return ChapterDetail(
            id=str(chapter.id),
            chapter_number=chapter.chapter_number,
            title=chapter.title,
            slug=chapter.slug,
            word_count=chapter.word_count,
            reading_time_minutes=chapter.reading_time_minutes,
            status=chapter.status.value,
            validation_errors=chapter.validation_errors or [],
            created_at=chapter.created_at.isoformat(),
            updated_at=chapter.updated_at.isoformat(),
            content_path=content_path,
            docusaurus_url=docusaurus_url,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get chapter {chapter_number}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chapter: {str(e)}",
        )


@router.delete(
    "/chapters/{chapter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a chapter",
    description="Delete a chapter and all its related content (cascade).",
)
async def delete_chapter(
    chapter_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete a chapter by ID.

    Args:
        chapter_id: Chapter UUID
        db: Database session

    Raises:
        HTTPException: If chapter not found
    """
    try:
        logger.info(f"Deleting chapter {chapter_id}")

        service = ChapterService(db)
        deleted = await service.delete_chapter(chapter_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter {chapter_id} not found",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete chapter {chapter_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete chapter: {str(e)}",
        )
