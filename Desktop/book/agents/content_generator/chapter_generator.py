"""Chapter content generation using LLM.

Generates AI-powered textbook chapters on Physical AI and Humanoid Robotics
with word count enforcement, retry logic, and validation.

Based on research.md and spec.md requirements.
"""

import logging
from typing import Optional
from dataclasses import dataclass

from agents.content_generator.curriculum import ChapterDefinition
from agents.content_generator.llm_client import LLMClient, GenerationError
from agents.content_generator.prompts import (
    CHAPTER_GENERATION_SYSTEM_PROMPT,
    get_chapter_generation_prompt,
)

logger = logging.getLogger(__name__)


@dataclass
class ChapterGenerationResult:
    """Result of chapter generation.

    Attributes:
        content: Generated chapter markdown content
        chapter_number: Chapter number
        chapter_title: Chapter title
        word_count: Actual word count
        tokens_used: Tokens consumed by generation
        model_used: LLM model identifier
        generation_attempts: Number of attempts before success
        validation_passed: Whether content passed validation
    """

    content: str
    chapter_number: int
    chapter_title: str
    word_count: int
    tokens_used: int
    model_used: str
    generation_attempts: int
    validation_passed: bool


class ChapterGenerator:
    """Generates textbook chapter content using LLM.

    Features:
    - Word count enforcement (800-1200 words per constitution)
    - Automatic retry if word count is violated
    - Structured markdown output
    - Learning objectives integration
    - Token usage tracking

    Based on tasks.md: T023 - ChapterGenerator class
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        max_generation_attempts: int = 3,
        enforce_word_count: bool = True,
    ):
        """Initialize the chapter generator.

        Args:
            llm_client: Optional LLM client (creates new one if not provided)
            max_generation_attempts: Max attempts for word count enforcement
            enforce_word_count: Whether to retry if word count is out of range
        """
        self.llm_client = llm_client or LLMClient()
        self.max_generation_attempts = max_generation_attempts
        self.enforce_word_count = enforce_word_count

        logger.info(
            f"ChapterGenerator initialized "
            f"(max_attempts={max_generation_attempts}, "
            f"enforce_word_count={enforce_word_count})"
        )

    def generate_chapter(
        self, chapter: ChapterDefinition
    ) -> ChapterGenerationResult:
        """Generate a complete chapter.

        Args:
            chapter: ChapterDefinition with topics and learning objectives

        Returns:
            ChapterGenerationResult with generated content and metadata

        Raises:
            GenerationError: If generation fails after all attempts
        """
        logger.info(f"Starting generation for Chapter {chapter.number}: {chapter.title}")

        # Generate user prompt
        user_prompt = get_chapter_generation_prompt(chapter)

        # Select model for chapter generation (Sonnet for quality)
        model = LLMClient.get_model_for_task("chapter")

        # Attempt generation with word count enforcement
        for attempt in range(1, self.max_generation_attempts + 1):
            try:
                logger.info(
                    f"Generation attempt {attempt}/{self.max_generation_attempts} "
                    f"for Chapter {chapter.number}"
                )

                # Generate content with rate limit buffer
                result = self.llm_client.generate_with_rate_limit_buffer(
                    prompt=user_prompt,
                    system_prompt=CHAPTER_GENERATION_SYSTEM_PROMPT,
                    model=model,
                    max_tokens=4096,
                    temperature=1.0,
                )

                content = result.content

                # Count words
                word_count = self._count_words(content)
                logger.info(
                    f"Chapter {chapter.number} generated: {word_count} words "
                    f"(target: {chapter.word_count_target})"
                )

                # Check word count compliance
                if self.enforce_word_count:
                    if not self._is_word_count_valid(word_count):
                        logger.warning(
                            f"Word count {word_count} out of range (800-1200), "
                            f"retrying (attempt {attempt}/{self.max_generation_attempts})"
                        )
                        if attempt < self.max_generation_attempts:
                            # Modify prompt to emphasize word count
                            user_prompt = self._add_word_count_emphasis(
                                user_prompt, word_count, chapter.word_count_target
                            )
                            continue
                        else:
                            logger.error(
                                f"Failed to generate valid word count after "
                                f"{self.max_generation_attempts} attempts"
                            )
                            # Accept the content anyway (will fail validation later)

                # Success - return result
                logger.info(
                    f"Chapter {chapter.number} generation successful "
                    f"(attempts: {attempt}, tokens: {result.tokens_used})"
                )

                return ChapterGenerationResult(
                    content=content,
                    chapter_number=chapter.number,
                    chapter_title=chapter.title,
                    word_count=word_count,
                    tokens_used=result.tokens_used,
                    model_used=result.model,
                    generation_attempts=attempt,
                    validation_passed=self._is_word_count_valid(word_count),
                )

            except GenerationError as e:
                logger.error(
                    f"Generation error on attempt {attempt} for Chapter {chapter.number}: {e}"
                )
                if attempt >= self.max_generation_attempts:
                    raise
                # Retry on next iteration

        # Should not reach here, but fail gracefully
        raise GenerationError(
            f"Failed to generate Chapter {chapter.number} after "
            f"{self.max_generation_attempts} attempts"
        )

    def _count_words(self, content: str) -> int:
        """Count words in markdown content.

        Args:
            content: Markdown content string

        Returns:
            Word count
        """
        # Simple word count (split by whitespace)
        # More sophisticated counting is done by validator
        words = content.split()
        return len(words)

    def _is_word_count_valid(self, word_count: int) -> bool:
        """Check if word count is within constitution limits.

        Args:
            word_count: Word count to validate

        Returns:
            True if word count is 800-1200
        """
        return 800 <= word_count <= 1200

    def _add_word_count_emphasis(
        self, original_prompt: str, actual_count: int, target_count: int
    ) -> str:
        """Add emphasis to prompt about word count requirements.

        Args:
            original_prompt: Original user prompt
            actual_count: Actual word count from previous attempt
            target_count: Target word count

        Returns:
            Modified prompt with stronger word count emphasis
        """
        if actual_count < 800:
            emphasis = f"\n\n**CRITICAL**: The previous attempt was too short ({actual_count} words). You MUST generate at least 800 words. Target is {target_count} words. Add more depth, examples, and explanations to reach the required length."
        else:
            emphasis = f"\n\n**CRITICAL**: The previous attempt was too long ({actual_count} words). You MUST stay under 1200 words. Target is {target_count} words. Be more concise and focused on core concepts."

        return original_prompt + emphasis

    def get_total_tokens_used(self) -> int:
        """Get total tokens used by this generator.

        Returns:
            Total tokens consumed
        """
        return self.llm_client.get_total_tokens_used()

    def reset_token_counter(self) -> None:
        """Reset the token usage counter."""
        self.llm_client.reset_token_counter()


# Utility function for quick chapter generation
def generate_chapter_by_number(
    chapter_number: int, llm_client: Optional[LLMClient] = None
) -> ChapterGenerationResult:
    """Generate a chapter by its number.

    Args:
        chapter_number: Chapter number (1-8)
        llm_client: Optional LLM client

    Returns:
        ChapterGenerationResult

    Raises:
        ValueError: If chapter number is invalid
        GenerationError: If generation fails
    """
    from agents.content_generator.curriculum import get_chapter_by_number

    chapter = get_chapter_by_number(chapter_number)
    generator = ChapterGenerator(llm_client=llm_client)
    return generator.generate_chapter(chapter)
