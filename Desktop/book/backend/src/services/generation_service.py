"""Generation orchestration service for textbook content.

Coordinates batch chapter generation with sequential execution, rate limiting,
and status tracking.

Based on tasks.md: T026 - GenerationService orchestration
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.generation_job import GenerationJob, JobStatus
from backend.src.models.chapter import ChapterStatus
from backend.src.services.chapter_service import ChapterService
from agents.content_generator.curriculum import get_curriculum, ChapterDefinition
from agents.content_generator.chapter_generator import ChapterGenerator, ChapterGenerationResult
from agents.content_generator.summary_generator import SummaryGenerator, SummaryGenerationResult
from agents.content_generator.validator import ContentValidator
from agents.content_generator.llm_client import LLMClient
from agents.content_generator.markdown_writer import MarkdownWriter

logger = logging.getLogger(__name__)


class GenerationService:
    """Orchestrates batch textbook content generation.

    Features:
    - Sequential chapter generation with rate limiting (5s delays)
    - Status tracking and progress updates
    - Token usage monitoring
    - Validation integration
    - Error handling and recovery

    Based on tasks.md: T026 - GenerationService orchestration
    """

    # Sequential generation delay (5 seconds between chapters per research)
    GENERATION_DELAY_SECONDS = 5

    def __init__(self, db_session: AsyncSession):
        """Initialize the service.

        Args:
            db_session: Async database session
        """
        self.db_session = db_session
        self.chapter_service = ChapterService(db_session)

    async def start_batch_generation(
        self,
        include_extended: bool = False,
        model_override: Optional[str] = None,
    ) -> UUID:
        """Start a new batch generation job for all chapters.

        Args:
            include_extended: If True, generate P2/P3 chapters (default: False for MVP)
            model_override: Optional model override (default: uses curriculum recommendations)

        Returns:
            UUID of the created generation job

        Raises:
            RuntimeError: If generation fails to start
        """
        curriculum = get_curriculum(include_extended=include_extended)
        chapters_total = len(curriculum)

        logger.info(
            f"Starting batch generation: {chapters_total} chapters "
            f"(extended={include_extended})"
        )

        # Create generation job
        job = GenerationJob(
            status=JobStatus.PENDING,
            chapters_completed=0,
            chapters_total=chapters_total,
            errors=[],
            token_usage=0,
            model_used=model_override or LLMClient.MODEL_SONNET,
        )

        self.db_session.add(job)
        await self.db_session.commit()
        await self.db_session.refresh(job)

        logger.info(f"Generation job created: {job.id}")

        # Start generation in background (non-blocking)
        asyncio.create_task(self._execute_batch_generation(job.id, curriculum))

        return job.id

    async def _execute_batch_generation(
        self,
        job_id: UUID,
        curriculum: List[ChapterDefinition],
    ) -> None:
        """Execute batch generation for all chapters (background task).

        Args:
            job_id: Generation job UUID
            curriculum: List of chapters to generate
        """
        try:
            logger.info(f"Executing batch generation for job {job_id}")

            # Update job status to IN_PROGRESS
            await self._update_job_status(job_id, JobStatus.IN_PROGRESS)

            # Initialize generator and validator
            llm_client = LLMClient()
            generator = ChapterGenerator(llm_client=llm_client)
            validator = ContentValidator()

            # Sequential generation with delays
            for i, chapter_def in enumerate(curriculum, start=1):
                try:
                    logger.info(
                        f"Generating chapter {i}/{len(curriculum)}: {chapter_def.title}"
                    )

                    # Generate chapter
                    result = generator.generate_chapter(chapter_def)

                    # Validate chapter
                    validation_result = validator.validate_chapter(result.content)

                    # Calculate reading time
                    reading_time = validation_result.metrics.get("reading_time_minutes", 6)

                    # Create chapter record
                    chapter = await self.chapter_service.create_chapter(
                        job_id=job_id,
                        chapter_number=chapter_def.number,
                        title=chapter_def.title,
                        slug=chapter_def.slug,
                        word_count=result.word_count,
                        reading_time_minutes=reading_time,
                        status=(
                            ChapterStatus.VALIDATED
                            if validation_result.valid
                            else ChapterStatus.FAILED
                        ),
                    )

                    # Update chapter with validation errors if any
                    if not validation_result.valid:
                        await self.chapter_service.update_chapter_status(
                            chapter.id,
                            ChapterStatus.FAILED,
                            validation_errors=validation_result.errors,
                        )
                        logger.warning(
                            f"Chapter {chapter_def.number} validation failed: "
                            f"{validation_result.errors}"
                        )

                    # Update job progress
                    await self._increment_job_progress(
                        job_id,
                        tokens_used=result.tokens_used,
                    )

                    logger.info(
                        f"Chapter {chapter_def.number} generated successfully "
                        f"(words: {result.word_count}, tokens: {result.tokens_used})"
                    )

                    # Apply rate limiting delay (except after last chapter)
                    if i < len(curriculum):
                        logger.debug(
                            f"Applying generation delay ({self.GENERATION_DELAY_SECONDS}s)"
                        )
                        await asyncio.sleep(self.GENERATION_DELAY_SECONDS)

                except Exception as e:
                    error_msg = f"Failed to generate chapter {chapter_def.number}: {e}"
                    logger.error(error_msg)
                    await self._add_job_error(job_id, error_msg)
                    # Continue with next chapter (don't fail entire job)

            # Generate summaries for all chapters (parallel generation)
            logger.info("Starting summary generation for all chapters")
            try:
                await self._generate_summaries_for_chapters(job_id, curriculum, llm_client)
            except Exception as e:
                error_msg = f"Summary generation failed: {e}"
                logger.error(error_msg)
                await self._add_job_error(job_id, error_msg)
                # Don't fail the job - chapters are already generated

            # Mark job as completed
            await self._complete_job(job_id)
            logger.info(f"Batch generation completed for job {job_id}")

        except Exception as e:
            error_msg = f"Batch generation failed: {e}"
            logger.error(error_msg)
            await self._fail_job(job_id, error_msg)

    async def _generate_summaries_for_chapters(
        self,
        job_id: UUID,
        curriculum: List[ChapterDefinition],
        llm_client: LLMClient,
    ) -> None:
        """Generate summaries for all chapters in parallel.

        Args:
            job_id: Generation job UUID
            curriculum: List of chapters
            llm_client: LLM client for generation
        """
        logger.info(f"Generating summaries for {len(curriculum)} chapters")

        # Initialize generators and writer
        summary_generator = SummaryGenerator(llm_client=llm_client)
        markdown_writer = MarkdownWriter()

        # Create summary generation tasks for all chapters
        summary_tasks = []
        for chapter_def in curriculum:
            task = self._generate_single_summary(
                chapter_def=chapter_def,
                summary_generator=summary_generator,
                markdown_writer=markdown_writer,
                job_id=job_id,
            )
            summary_tasks.append(task)

        # Execute all summary generations in parallel
        results = await asyncio.gather(*summary_tasks, return_exceptions=True)

        # Log results
        successful = sum(1 for r in results if not isinstance(r, Exception))
        failed = len(results) - successful

        logger.info(
            f"Summary generation complete: {successful} successful, {failed} failed"
        )

        if failed > 0:
            error_msg = f"Failed to generate summaries for {failed} chapters"
            logger.warning(error_msg)
            await self._add_job_error(job_id, error_msg)

    async def _generate_single_summary(
        self,
        chapter_def: ChapterDefinition,
        summary_generator: SummaryGenerator,
        markdown_writer: MarkdownWriter,
        job_id: UUID,
    ) -> SummaryGenerationResult:
        """Generate summary for a single chapter.

        Args:
            chapter_def: Chapter definition
            summary_generator: Summary generator instance
            markdown_writer: Markdown writer instance
            job_id: Generation job UUID

        Returns:
            SummaryGenerationResult

        Raises:
            Exception: If summary generation or writing fails
        """
        try:
            logger.info(f"Generating summary for Chapter {chapter_def.number}")

            # Read the generated chapter content from markdown file
            file_path = markdown_writer.get_chapter_file_path(
                chapter_def.number, chapter_def.slug
            )

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Chapter file not found: {file_path}. "
                    f"Chapter must be generated before summary."
                )

            # Read chapter content
            chapter_content = file_path.read_text(encoding="utf-8")

            # Generate summary (runs in thread pool since it's synchronous)
            result = await asyncio.to_thread(
                summary_generator.generate_summary,
                chapter_content=chapter_content,
                chapter_title=chapter_def.title,
                chapter_number=chapter_def.number,
            )

            # Append summary to chapter markdown file
            await asyncio.to_thread(
                markdown_writer.append_summary_to_chapter,
                chapter_number=chapter_def.number,
                slug=chapter_def.slug,
                takeaways=result.takeaways,
            )

            logger.info(
                f"Summary for Chapter {chapter_def.number} generated and appended "
                f"({len(result.takeaways)} takeaways, {result.tokens_used} tokens, "
                f"valid: {result.validation_passed})"
            )

            # Track token usage
            await self._increment_job_progress(job_id, tokens_used=result.tokens_used)

            return result

        except Exception as e:
            logger.error(f"Failed to generate summary for Chapter {chapter_def.number}: {e}")
            raise

    async def get_job_status(self, job_id: UUID) -> Optional[dict]:
        """Get the status of a generation job.

        Args:
            job_id: Generation job UUID

        Returns:
            Dictionary with job status and progress, or None if not found
        """
        job = await self._get_job(job_id)
        if not job:
            return None

        return {
            "job_id": str(job.id),
            "status": job.status.value,
            "progress": {
                "chapters_completed": job.chapters_completed,
                "chapters_total": job.chapters_total,
                "percentage": job.progress_percentage,
            },
            "started_at": job.started_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "token_usage": job.token_usage,
            "model_used": job.model_used,
            "errors": job.errors,
            "is_complete": job.is_complete,
        }

    async def cancel_job(self, job_id: UUID) -> bool:
        """Cancel a running generation job.

        Note: This only updates the status; actual task cancellation
        is not implemented (tasks run to completion).

        Args:
            job_id: Generation job UUID

        Returns:
            True if cancelled, False if not found or already complete
        """
        job = await self._get_job(job_id)
        if not job:
            return False

        if job.is_complete:
            logger.warning(f"Cannot cancel completed job {job_id}")
            return False

        logger.info(f"Cancelling job {job_id}")
        job.status = JobStatus.FAILED
        job.completed_at = datetime.utcnow()
        job.add_error("Job cancelled by user")

        await self.db_session.commit()
        return True

    # Private helper methods

    async def _get_job(self, job_id: UUID) -> Optional[GenerationJob]:
        """Get a generation job by ID.

        Args:
            job_id: Job UUID

        Returns:
            GenerationJob or None
        """
        return await self.db_session.get(GenerationJob, job_id)

    async def _update_job_status(self, job_id: UUID, new_status: JobStatus) -> None:
        """Update job status.

        Args:
            job_id: Job UUID
            new_status: New status to set
        """
        job = await self._get_job(job_id)
        if job:
            logger.info(
                f"Job {job_id} status: {job.status.value} -> {new_status.value}"
            )
            job.status = new_status
            await self.db_session.commit()

    async def _increment_job_progress(
        self, job_id: UUID, tokens_used: int
    ) -> None:
        """Increment job progress counters.

        Args:
            job_id: Job UUID
            tokens_used: Tokens consumed in this chapter
        """
        job = await self._get_job(job_id)
        if job:
            job.chapters_completed += 1
            job.token_usage += tokens_used
            await self.db_session.commit()
            logger.debug(
                f"Job {job_id} progress: {job.chapters_completed}/{job.chapters_total}"
            )

    async def _add_job_error(self, job_id: UUID, error_message: str) -> None:
        """Add an error to the job.

        Args:
            job_id: Job UUID
            error_message: Error description
        """
        job = await self._get_job(job_id)
        if job:
            job.add_error(error_message)
            await self.db_session.commit()

    async def _complete_job(self, job_id: UUID) -> None:
        """Mark a job as completed.

        Args:
            job_id: Job UUID
        """
        job = await self._get_job(job_id)
        if job:
            logger.info(f"Completing job {job_id}")
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            await self.db_session.commit()

    async def _fail_job(self, job_id: UUID, error_message: str) -> None:
        """Mark a job as failed.

        Args:
            job_id: Job UUID
            error_message: Failure reason
        """
        job = await self._get_job(job_id)
        if job:
            logger.error(f"Failing job {job_id}: {error_message}")
            job.status = JobStatus.FAILED
            job.completed_at = datetime.utcnow()
            job.add_error(error_message)
            await self.db_session.commit()
