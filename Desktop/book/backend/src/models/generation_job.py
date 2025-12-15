"""Generation Job model for tracking batch content generation.

Maps to the 'generation_jobs' table in the database.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Integer, String, TIMESTAMP, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum

from .base import Base


class JobStatus(str, enum.Enum):
    """Status of a generation job."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationJob(Base):
    """Tracks batch content generation jobs.

    Each job represents a complete textbook generation run that creates
    multiple chapters with their enhancements (summaries, quizzes, boosters).

    Constitution Compliance:
    - Tracks token usage for cost monitoring (Principle III: Free-Tier Architecture)
    - Records errors for observability (Principle VIII: Observability)
    - Enforces chapters_completed <= chapters_total constraint

    Attributes:
        id: Unique identifier (UUID)
        started_at: Timestamp when job was created
        completed_at: Timestamp when job finished (null if in progress)
        status: Current job status (pending/in_progress/completed/failed)
        chapters_completed: Number of chapters successfully generated
        chapters_total: Target number of chapters to generate (6-8)
        errors: List of error messages encountered (JSONB array)
        token_usage: Total tokens consumed by LLM API calls
        model_used: LLM model identifier used for generation
        chapters: Related Chapter objects
    """

    __tablename__ = "generation_jobs"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    # Status tracking
    status: Mapped[JobStatus] = mapped_column(
        SQLEnum(JobStatus, name="job_status", create_constraint=True),
        nullable=False,
        server_default="pending"
    )

    # Progress tracking
    chapters_completed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0"
    )
    chapters_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Error tracking
    errors: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        server_default="[]"
    )

    # Resource usage tracking
    token_usage: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0"
    )
    model_used: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Relationships
    chapters: Mapped[List["Chapter"]] = relationship(
        "Chapter",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "chapters_completed <= chapters_total",
            name="check_chapters_completed"
        ),
        CheckConstraint(
            "token_usage >= 0",
            name="check_token_usage"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<GenerationJob(id={self.id}, status={self.status.value}, "
            f"progress={self.chapters_completed}/{self.chapters_total})>"
        )

    @property
    def is_complete(self) -> bool:
        """Check if the job has finished (successfully or failed)."""
        return self.status in (JobStatus.COMPLETED, JobStatus.FAILED)

    @property
    def progress_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.chapters_total == 0:
            return 0.0
        return (self.chapters_completed / self.chapters_total) * 100

    def add_error(self, error_message: str) -> None:
        """Add an error message to the errors list.

        Args:
            error_message: Error description to record
        """
        if self.errors is None:
            self.errors = []
        self.errors.append({
            "message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        })
