"""Database models for textbook content generation.

This package contains SQLAlchemy ORM models that map to the database schema
defined in alembic/versions/001_initial_schema.py.

Models:
- GenerationJob: Tracks batch content generation jobs
- Chapter: Chapter metadata and status
- ChapterContent: Markdown file references
- Summary: AI-generated chapter summaries
- Quiz: Quiz collections per chapter
- QuizQuestion: Individual quiz questions
- LearningBooster: Supplementary learning content
"""

from .base import Base
from .generation_job import GenerationJob
from .chapter import Chapter, ChapterContent
from .summary import Summary
from .quiz import Quiz, QuizQuestion
from .learning_booster import LearningBooster

__all__ = [
    "Base",
    "GenerationJob",
    "Chapter",
    "ChapterContent",
    "Summary",
    "Quiz",
    "QuizQuestion",
    "LearningBooster",
]
