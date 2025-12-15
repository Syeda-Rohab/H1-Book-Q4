"""Chapter service for CRUD operations and status tracking.

Provides business logic layer for chapter management, abstracting database operations.
"""

import hashlib
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.src.models.chapter import Chapter, ChapterContent, ChapterStatus

logger = logging.getLogger(__name__)


class ChapterService:
    """Service for managing chapters and their content.

    Provides CRUD operations, status tracking, and constitution compliance checks.

    Based on tasks.md: T025 - ChapterService CRUD operations
    """

    def __init__(self, db_session: AsyncSession):
        """Initialize the service.

        Args:
            db_session: Async database session
        """
        self.db_session = db_session

    async def create_chapter(
        self,
        job_id: UUID,
        chapter_number: int,
        title: str,
        slug: str,
        word_count: int,
        reading_time_minutes: int,
        status: ChapterStatus = ChapterStatus.PENDING,
    ) -> Chapter:
        """Create a new chapter record.

        Args:
            job_id: ID of the generation job
            chapter_number: Chapter number (1-8)
            title: Chapter title
            slug: URL-friendly slug
            word_count: Total word count
            reading_time_minutes: Estimated reading time
            status: Initial status (default: PENDING)

        Returns:
            Created Chapter object

        Raises:
            ValueError: If constitution constraints are violated
            IntegrityError: If chapter_number or slug already exists
        """
        logger.info(f"Creating chapter {chapter_number}: {title}")

        # Validate constitution constraints
        if not (800 <= word_count <= 1200):
            raise ValueError(
                f"Word count {word_count} outside range (800-1200)"
            )
        if not (5 <= reading_time_minutes <= 7):
            raise ValueError(
                f"Reading time {reading_time_minutes} outside range (5-7 minutes)"
            )
        if not (1 <= chapter_number <= 8):
            raise ValueError(
                f"Chapter number {chapter_number} outside range (1-8)"
            )

        chapter = Chapter(
            job_id=job_id,
            chapter_number=chapter_number,
            title=title,
            slug=slug,
            word_count=word_count,
            reading_time_minutes=reading_time_minutes,
            status=status,
            validation_errors=[],
        )

        try:
            self.db_session.add(chapter)
            await self.db_session.commit()
            await self.db_session.refresh(chapter)
            logger.info(f"Chapter {chapter_number} created with ID {chapter.id}")
            return chapter
        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(f"Failed to create chapter {chapter_number}: {e}")
            raise

    async def get_chapter_by_id(self, chapter_id: UUID) -> Optional[Chapter]:
        """Get a chapter by its ID.

        Args:
            chapter_id: Chapter UUID

        Returns:
            Chapter object or None if not found
        """
        result = await self.db_session.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        return result.scalar_one_or_none()

    async def get_chapter_by_number(self, chapter_number: int) -> Optional[Chapter]:
        """Get a chapter by its number.

        Args:
            chapter_number: Chapter number (1-8)

        Returns:
            Chapter object or None if not found
        """
        result = await self.db_session.execute(
            select(Chapter).where(Chapter.chapter_number == chapter_number)
        )
        return result.scalar_one_or_none()

    async def get_chapter_by_slug(self, slug: str) -> Optional[Chapter]:
        """Get a chapter by its slug.

        Args:
            slug: URL-friendly slug

        Returns:
            Chapter object or None if not found
        """
        result = await self.db_session.execute(
            select(Chapter).where(Chapter.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list_all_chapters(self) -> List[Chapter]:
        """Get all chapters ordered by chapter_number.

        Returns:
            List of Chapter objects
        """
        result = await self.db_session.execute(
            select(Chapter).order_by(Chapter.chapter_number)
        )
        return list(result.scalars().all())

    async def list_chapters_by_status(self, status: ChapterStatus) -> List[Chapter]:
        """Get chapters filtered by status.

        Args:
            status: Chapter status to filter by

        Returns:
            List of Chapter objects
        """
        result = await self.db_session.execute(
            select(Chapter)
            .where(Chapter.status == status)
            .order_by(Chapter.chapter_number)
        )
        return list(result.scalars().all())

    async def update_chapter_status(
        self,
        chapter_id: UUID,
        new_status: ChapterStatus,
        validation_errors: Optional[List[str]] = None,
    ) -> Chapter:
        """Update chapter status and validation errors.

        Args:
            chapter_id: Chapter UUID
            new_status: New status to set
            validation_errors: Optional list of validation error messages

        Returns:
            Updated Chapter object

        Raises:
            ValueError: If chapter not found
        """
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            raise ValueError(f"Chapter {chapter_id} not found")

        logger.info(
            f"Updating chapter {chapter.chapter_number} status: "
            f"{chapter.status.value} -> {new_status.value}"
        )

        chapter.status = new_status

        if validation_errors:
            chapter.validation_errors = [
                {"message": err, "timestamp": datetime.utcnow().isoformat()}
                for err in validation_errors
            ]

        await self.db_session.commit()
        await self.db_session.refresh(chapter)
        return chapter

    async def add_chapter_content(
        self,
        chapter_id: UUID,
        markdown_path: str,
        content_text: str,
        docusaurus_url: str,
    ) -> ChapterContent:
        """Add content file metadata for a chapter.

        Args:
            chapter_id: Chapter UUID
            markdown_path: Path to markdown file
            content_text: Full markdown content (for hashing)
            docusaurus_url: Public URL in Docusaurus

        Returns:
            Created ChapterContent object

        Raises:
            ValueError: If chapter not found
            IntegrityError: If content already exists for this chapter
        """
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            raise ValueError(f"Chapter {chapter_id} not found")

        # Compute content hash (SHA-256)
        content_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()

        logger.info(
            f"Adding content for chapter {chapter.chapter_number} "
            f"(path: {markdown_path})"
        )

        content = ChapterContent(
            chapter_id=chapter_id,
            markdown_path=markdown_path,
            content_hash=content_hash,
            docusaurus_url=docusaurus_url,
        )

        try:
            self.db_session.add(content)
            await self.db_session.commit()
            await self.db_session.refresh(content)
            logger.info(f"Content added for chapter {chapter.chapter_number}")
            return content
        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(
                f"Failed to add content for chapter {chapter.chapter_number}: {e}"
            )
            raise

    async def delete_chapter(self, chapter_id: UUID) -> bool:
        """Delete a chapter and all related content (cascade).

        Args:
            chapter_id: Chapter UUID

        Returns:
            True if deleted, False if chapter not found
        """
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            logger.warning(f"Attempted to delete non-existent chapter {chapter_id}")
            return False

        logger.info(
            f"Deleting chapter {chapter.chapter_number}: {chapter.title}"
        )

        await self.db_session.delete(chapter)
        await self.db_session.commit()
        logger.info(f"Chapter {chapter.chapter_number} deleted")
        return True

    async def count_chapters(self) -> int:
        """Count total chapters in the database.

        Returns:
            Total chapter count
        """
        result = await self.db_session.execute(select(Chapter))
        return len(list(result.scalars().all()))

    async def validate_constitution_compliance(self, chapter_id: UUID) -> List[str]:
        """Validate that a chapter meets constitution requirements.

        Args:
            chapter_id: Chapter UUID

        Returns:
            List of validation errors (empty if compliant)

        Raises:
            ValueError: If chapter not found
        """
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            raise ValueError(f"Chapter {chapter_id} not found")

        errors = []

        # Check word count (Principle VII: Content Quality Over Quantity)
        if not (800 <= chapter.word_count <= 1200):
            errors.append(
                f"Word count {chapter.word_count} outside range (800-1200)"
            )

        # Check reading time
        if not (5 <= chapter.reading_time_minutes <= 7):
            errors.append(
                f"Reading time {chapter.reading_time_minutes} outside range (5-7 min)"
            )

        # Check chapter number
        if not (1 <= chapter.chapter_number <= 8):
            errors.append(
                f"Chapter number {chapter.chapter_number} outside range (1-8)"
            )

        return errors
