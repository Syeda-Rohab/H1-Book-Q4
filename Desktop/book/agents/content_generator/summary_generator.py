"""Summary generation for textbook chapters using LLM.

Generates AI-powered chapter summaries with 3-5 key takeaways
using the Haiku model for faster/cheaper generation.

Based on tasks.md: T039 - SummaryGenerator class
"""

import json
import logging
from typing import Optional, List
from dataclasses import dataclass

from agents.content_generator.llm_client import LLMClient, GenerationError
from agents.content_generator.prompts import (
    SUMMARY_GENERATION_SYSTEM_PROMPT,
    get_summary_generation_prompt,
)
from agents.content_generator.validator import ContentValidator, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class SummaryGenerationResult:
    """Result of summary generation.

    Attributes:
        takeaways: List of 3-5 key takeaway strings (50-150 chars each)
        chapter_number: Chapter number
        chapter_title: Chapter title
        tokens_used: Tokens consumed by generation
        model_used: LLM model identifier
        generation_attempts: Number of attempts before success
        validation_passed: Whether content passed validation
    """

    takeaways: List[str]
    chapter_number: int
    chapter_title: str
    tokens_used: int
    model_used: str
    generation_attempts: int
    validation_passed: bool


class SummaryGenerator:
    """Generates chapter summaries using LLM.

    Features:
    - Generates 3-5 key takeaways per chapter
    - Each takeaway is 50-150 characters
    - Uses Haiku model (faster/cheaper than Sonnet)
    - Automatic retry if validation fails
    - JSON parsing with error handling
    - Token usage tracking

    Based on tasks.md: T039 - SummaryGenerator class
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        validator: Optional[ContentValidator] = None,
        max_generation_attempts: int = 3,
        enforce_validation: bool = True,
    ):
        """Initialize the summary generator.

        Args:
            llm_client: Optional LLM client (creates new one if not provided)
            validator: Optional validator (creates new one if not provided)
            max_generation_attempts: Max attempts for valid summary generation
            enforce_validation: Whether to retry if validation fails
        """
        self.llm_client = llm_client or LLMClient()
        self.validator = validator or ContentValidator()
        self.max_generation_attempts = max_generation_attempts
        self.enforce_validation = enforce_validation

        logger.info(
            f"SummaryGenerator initialized "
            f"(max_attempts={max_generation_attempts}, "
            f"enforce_validation={enforce_validation})"
        )

    def generate_summary(
        self,
        chapter_content: str,
        chapter_title: str,
        chapter_number: int,
    ) -> SummaryGenerationResult:
        """Generate a summary with 3-5 key takeaways for a chapter.

        Args:
            chapter_content: Full chapter markdown content
            chapter_title: Chapter title
            chapter_number: Chapter number

        Returns:
            SummaryGenerationResult with takeaways and metadata

        Raises:
            GenerationError: If generation fails after all attempts
        """
        logger.info(f"Starting summary generation for Chapter {chapter_number}: {chapter_title}")

        # Generate user prompt
        user_prompt = get_summary_generation_prompt(chapter_content, chapter_title)

        # Select model for summary generation (Haiku for speed/cost)
        model = LLMClient.get_model_for_task("summary")

        # Attempt generation with validation enforcement
        for attempt in range(1, self.max_generation_attempts + 1):
            try:
                logger.info(
                    f"Summary generation attempt {attempt}/{self.max_generation_attempts} "
                    f"for Chapter {chapter_number}"
                )

                # Generate content with rate limit buffer
                result = self.llm_client.generate_with_rate_limit_buffer(
                    prompt=user_prompt,
                    system_prompt=SUMMARY_GENERATION_SYSTEM_PROMPT,
                    model=model,
                    max_tokens=1024,  # Smaller than chapters (summaries are concise)
                    temperature=1.0,
                )

                content = result.content.strip()

                # Parse JSON response
                try:
                    takeaways = self._parse_takeaways_json(content)
                except (json.JSONDecodeError, ValueError) as e:
                    logger.warning(
                        f"Failed to parse JSON response on attempt {attempt}: {e}"
                    )
                    if attempt < self.max_generation_attempts:
                        # Modify prompt to emphasize JSON format
                        user_prompt = self._add_json_format_emphasis(user_prompt)
                        continue
                    else:
                        raise GenerationError(
                            f"Failed to parse summary JSON after {self.max_generation_attempts} attempts"
                        ) from e

                logger.info(
                    f"Chapter {chapter_number} summary parsed: {len(takeaways)} takeaways "
                    f"(tokens: {result.tokens_used})"
                )

                # Validate summary
                validation_result = self.validator.validate_summary(takeaways)

                if self.enforce_validation and not validation_result.valid:
                    logger.warning(
                        f"Summary validation failed on attempt {attempt}: "
                        f"{validation_result.errors}"
                    )
                    if attempt < self.max_generation_attempts:
                        # Modify prompt to emphasize validation requirements
                        user_prompt = self._add_validation_emphasis(
                            user_prompt, validation_result
                        )
                        continue
                    else:
                        logger.error(
                            f"Failed to generate valid summary after "
                            f"{self.max_generation_attempts} attempts"
                        )
                        # Accept the content anyway (will fail validation in logs)

                # Success - return result
                logger.info(
                    f"Chapter {chapter_number} summary generation successful "
                    f"(attempts: {attempt}, tokens: {result.tokens_used}, "
                    f"valid: {validation_result.valid})"
                )

                return SummaryGenerationResult(
                    takeaways=takeaways,
                    chapter_number=chapter_number,
                    chapter_title=chapter_title,
                    tokens_used=result.tokens_used,
                    model_used=result.model,
                    generation_attempts=attempt,
                    validation_passed=validation_result.valid,
                )

            except GenerationError as e:
                logger.error(
                    f"Generation error on attempt {attempt} for Chapter {chapter_number}: {e}"
                )
                if attempt >= self.max_generation_attempts:
                    raise
                # Retry on next iteration

        # Should not reach here, but fail gracefully
        raise GenerationError(
            f"Failed to generate summary for Chapter {chapter_number} after "
            f"{self.max_generation_attempts} attempts"
        )

    def _parse_takeaways_json(self, content: str) -> List[str]:
        """Parse JSON array of takeaways from LLM response.

        Args:
            content: LLM response content (should be JSON array)

        Returns:
            List of takeaway strings

        Raises:
            ValueError: If JSON is invalid or not an array of strings
        """
        # Try to extract JSON from markdown code blocks if present
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        if content.startswith("```"):
            content = content[3:]  # Remove ```
        if content.endswith("```"):
            content = content[:-3]  # Remove trailing ```
        content = content.strip()

        # Parse JSON
        parsed = json.loads(content)

        # Validate it's a list
        if not isinstance(parsed, list):
            raise ValueError(f"Expected JSON array, got {type(parsed)}")

        # Validate all items are strings
        if not all(isinstance(item, str) for item in parsed):
            raise ValueError("All takeaways must be strings")

        return parsed

    def _add_json_format_emphasis(self, original_prompt: str) -> str:
        """Add emphasis to prompt about JSON format requirements.

        Args:
            original_prompt: Original user prompt

        Returns:
            Modified prompt with stronger JSON format emphasis
        """
        emphasis = (
            '\n\n**CRITICAL**: Your response MUST be a valid JSON array of strings. '
            'Example format:\n["Takeaway 1", "Takeaway 2", "Takeaway 3"]\n'
            'Do NOT include any markdown formatting, code blocks, or explanations. '
            'Return ONLY the JSON array.'
        )
        return original_prompt + emphasis

    def _add_validation_emphasis(
        self, original_prompt: str, validation_result: ValidationResult
    ) -> str:
        """Add emphasis to prompt about validation requirements.

        Args:
            original_prompt: Original user prompt
            validation_result: ValidationResult with errors

        Returns:
            Modified prompt with validation error feedback
        """
        errors_text = "; ".join(validation_result.errors)
        emphasis = (
            f'\n\n**CRITICAL**: The previous attempt failed validation with these errors: '
            f'{errors_text}\n\n'
            f'Requirements:\n'
            f'- Generate exactly 3-5 takeaways\n'
            f'- Each takeaway must be 50-150 characters\n'
            f'- Return as JSON array: ["Takeaway 1", "Takeaway 2", ...]\n'
            f'Please fix these issues and try again.'
        )
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


# Utility function for quick summary generation
def generate_summary_for_chapter(
    chapter_content: str,
    chapter_title: str,
    chapter_number: int,
    llm_client: Optional[LLMClient] = None,
) -> SummaryGenerationResult:
    """Generate a summary for a chapter.

    Args:
        chapter_content: Full chapter markdown content
        chapter_title: Chapter title
        chapter_number: Chapter number
        llm_client: Optional LLM client

    Returns:
        SummaryGenerationResult with takeaways

    Raises:
        GenerationError: If generation fails
    """
    generator = SummaryGenerator(llm_client=llm_client)
    return generator.generate_summary(
        chapter_content=chapter_content,
        chapter_title=chapter_title,
        chapter_number=chapter_number,
    )
