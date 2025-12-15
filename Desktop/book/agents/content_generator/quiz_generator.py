"""Quiz generation for textbook chapters using LLM.

Generates AI-powered quiz questions (5-7 multiple choice) per chapter
using the Haiku model for faster/cheaper generation.

Based on tasks.md: T047 - QuizGenerator class
"""

import json
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from agents.content_generator.llm_client import LLMClient, GenerationError
from agents.content_generator.prompts import (
    QUIZ_GENERATION_SYSTEM_PROMPT,
    get_quiz_generation_prompt,
)
from agents.content_generator.validator import ContentValidator, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class QuizGenerationResult:
    """Result of quiz generation.

    Attributes:
        questions: List of quiz question dictionaries
        chapter_number: Chapter number
        chapter_title: Chapter title
        tokens_used: Tokens consumed by generation
        model_used: LLM model identifier
        generation_attempts: Number of attempts before success
        validation_passed: Whether content passed validation
    """

    questions: List[Dict[str, Any]]
    chapter_number: int
    chapter_title: str
    tokens_used: int
    model_used: str
    generation_attempts: int
    validation_passed: bool


class QuizGenerator:
    """Generates quiz questions using LLM.

    Features:
    - Generates 5-7 multiple choice questions per chapter
    - Each question has exactly 4 options
    - Exactly 1 correct answer per question
    - Uses Haiku model (faster/cheaper than Sonnet)
    - Automatic retry if validation fails
    - JSON parsing with error handling
    - Token usage tracking
    - Difficulty mix (easy, medium, hard)

    Based on tasks.md: T047 - QuizGenerator class
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        validator: Optional[ContentValidator] = None,
        max_generation_attempts: int = 3,
        enforce_validation: bool = True,
        num_questions: int = 5,
    ):
        """Initialize the quiz generator.

        Args:
            llm_client: Optional LLM client (creates new one if not provided)
            validator: Optional validator (creates new one if not provided)
            max_generation_attempts: Max attempts for valid quiz generation
            enforce_validation: Whether to retry if validation fails
            num_questions: Number of questions to generate (default: 5, range: 5-7)
        """
        self.llm_client = llm_client or LLMClient()
        self.validator = validator or ContentValidator()
        self.max_generation_attempts = max_generation_attempts
        self.enforce_validation = enforce_validation
        self.num_questions = max(5, min(7, num_questions))  # Clamp to 5-7

        logger.info(
            f"QuizGenerator initialized "
            f"(max_attempts={max_generation_attempts}, "
            f"enforce_validation={enforce_validation}, "
            f"num_questions={self.num_questions})"
        )

    def generate_quiz(
        self,
        chapter_content: str,
        chapter_title: str,
        chapter_number: int,
    ) -> QuizGenerationResult:
        """Generate a quiz with 5-7 questions for a chapter.

        Args:
            chapter_content: Full chapter markdown content
            chapter_title: Chapter title
            chapter_number: Chapter number

        Returns:
            QuizGenerationResult with questions and metadata

        Raises:
            GenerationError: If generation fails after all attempts
        """
        logger.info(
            f"Starting quiz generation for Chapter {chapter_number}: {chapter_title} "
            f"({self.num_questions} questions)"
        )

        # Generate user prompt
        user_prompt = get_quiz_generation_prompt(
            chapter_content, chapter_title, self.num_questions
        )

        # Select model for quiz generation (Haiku for speed/cost)
        model = LLMClient.get_model_for_task("quiz")

        # Attempt generation with validation enforcement
        for attempt in range(1, self.max_generation_attempts + 1):
            try:
                logger.info(
                    f"Quiz generation attempt {attempt}/{self.max_generation_attempts} "
                    f"for Chapter {chapter_number}"
                )

                # Generate content with rate limit buffer
                result = self.llm_client.generate_with_rate_limit_buffer(
                    prompt=user_prompt,
                    system_prompt=QUIZ_GENERATION_SYSTEM_PROMPT,
                    model=model,
                    max_tokens=2048,  # Larger than summaries (quizzes have more content)
                    temperature=1.0,
                )

                content = result.content.strip()

                # Parse JSON response
                try:
                    questions = self._parse_quiz_json(content)
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
                            f"Failed to parse quiz JSON after {self.max_generation_attempts} attempts"
                        ) from e

                logger.info(
                    f"Chapter {chapter_number} quiz parsed: {len(questions)} questions "
                    f"(tokens: {result.tokens_used})"
                )

                # Validate quiz
                validation_result = self.validator.validate_quiz(
                    questions, min_questions=self.num_questions, max_questions=self.num_questions
                )

                if self.enforce_validation and not validation_result.valid:
                    logger.warning(
                        f"Quiz validation failed on attempt {attempt}: "
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
                            f"Failed to generate valid quiz after "
                            f"{self.max_generation_attempts} attempts"
                        )
                        # Accept the content anyway (will fail validation in logs)

                # Success - return result
                logger.info(
                    f"Chapter {chapter_number} quiz generation successful "
                    f"(attempts: {attempt}, tokens: {result.tokens_used}, "
                    f"questions: {len(questions)}, valid: {validation_result.valid})"
                )

                return QuizGenerationResult(
                    questions=questions,
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
            f"Failed to generate quiz for Chapter {chapter_number} after "
            f"{self.max_generation_attempts} attempts"
        )

    def _parse_quiz_json(self, content: str) -> List[Dict[str, Any]]:
        """Parse JSON array of quiz questions from LLM response.

        Args:
            content: LLM response content (should be JSON array)

        Returns:
            List of question dictionaries

        Raises:
            ValueError: If JSON is invalid or not properly formatted
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

        # Validate all items are dictionaries with required fields
        required_fields = {"question_text", "options", "correct_index"}
        for i, item in enumerate(parsed):
            if not isinstance(item, dict):
                raise ValueError(f"Question {i+1} is not a dictionary")

            missing_fields = required_fields - set(item.keys())
            if missing_fields:
                raise ValueError(
                    f"Question {i+1} missing required fields: {missing_fields}"
                )

        return parsed

    def _add_json_format_emphasis(self, original_prompt: str) -> str:
        """Add emphasis to prompt about JSON format requirements.

        Args:
            original_prompt: Original user prompt

        Returns:
            Modified prompt with stronger JSON format emphasis
        """
        emphasis = (
            '\n\n**CRITICAL**: Your response MUST be a valid JSON array of question objects. '
            'Example format:\n'
            '[{"question_text": "...", "options": ["A", "B", "C", "D"], "correct_index": 0, '
            '"difficulty": "easy", "topic": "..."}]\n'
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
            f'- Generate exactly {self.num_questions} questions\n'
            f'- Each question must have exactly 4 options\n'
            f'- Each question must have exactly 1 correct answer (correct_index: 0-3)\n'
            f'- All question_text fields must be non-empty\n'
            f'- All options must be non-empty strings\n'
            f'- Return as JSON array with required fields\n'
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


# Utility function for quick quiz generation
def generate_quiz_for_chapter(
    chapter_content: str,
    chapter_title: str,
    chapter_number: int,
    num_questions: int = 5,
    llm_client: Optional[LLMClient] = None,
) -> QuizGenerationResult:
    """Generate a quiz for a chapter.

    Args:
        chapter_content: Full chapter markdown content
        chapter_title: Chapter title
        chapter_number: Chapter number
        num_questions: Number of questions (5-7)
        llm_client: Optional LLM client

    Returns:
        QuizGenerationResult with questions

    Raises:
        GenerationError: If generation fails
    """
    generator = QuizGenerator(
        llm_client=llm_client, num_questions=num_questions
    )
    return generator.generate_quiz(
        chapter_content=chapter_content,
        chapter_title=chapter_title,
        chapter_number=chapter_number,
    )
