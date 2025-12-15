"""Content validation framework for textbook generation.

Validates markdown syntax, word counts, content structure, and constitution compliance.

Based on research.md: Research Task 3 - Content Validation Strategy
"""

import re
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from markdown_it import MarkdownIt

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of content validation.

    Attributes:
        valid: True if content passes all validation checks
        errors: List of validation error messages
        warnings: List of validation warnings (non-blocking)
        metrics: Dictionary of content metrics (word count, etc.)
    """

    valid: bool
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]

    def __repr__(self) -> str:
        status = "VALID" if self.valid else "INVALID"
        return (
            f"<ValidationResult({status}, "
            f"errors={len(self.errors)}, warnings={len(self.warnings)})>"
        )


class ContentValidator:
    """Validates textbook content for constitution compliance.

    Validation Layers:
    1. Markdown syntax validation (markdown-it-py)
    2. Content structure validation (headers, sections)
    3. Word count validation (800-1200 words)
    4. Constitution compliance checks

    Constitution Requirements:
    - Word count: 800-1200 words per chapter
    - Reading time: 5-7 minutes (calculated from word count)
    - Structure: H1 title, learning objectives, proper sections
    """

    # Constitution constraints
    MIN_WORD_COUNT = 800
    MAX_WORD_COUNT = 1200
    MIN_READING_TIME = 5  # minutes
    MAX_READING_TIME = 7  # minutes
    AVERAGE_READING_SPEED = 200  # words per minute

    def __init__(self):
        """Initialize the validator."""
        self.md_parser = MarkdownIt()
        logger.info("ContentValidator initialized")

    def validate_chapter(self, content: str) -> ValidationResult:
        """Validate a complete chapter.

        Args:
            content: Markdown content string

        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        metrics = {}

        # Layer 1: Markdown syntax validation
        syntax_errors = self._validate_markdown_syntax(content)
        errors.extend(syntax_errors)

        # Layer 2: Content structure validation
        structure_errors = self._validate_structure(content)
        errors.extend(structure_errors)

        # Layer 3: Word count validation
        word_count = self._count_words(content)
        metrics["word_count"] = word_count

        word_count_errors = self._validate_word_count(word_count)
        errors.extend(word_count_errors)

        # Calculate reading time
        reading_time = self._calculate_reading_time(word_count)
        metrics["reading_time_minutes"] = reading_time

        reading_time_errors = self._validate_reading_time(reading_time)
        errors.extend(reading_time_errors)

        # Layer 4: Learning objectives validation
        objectives = self._extract_learning_objectives(content)
        metrics["learning_objectives_count"] = len(objectives)

        if len(objectives) == 0:
            warnings.append("No learning objectives section found")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
        )

    def validate_summary(
        self, takeaways: List[str], min_count: int = 3, max_count: int = 5
    ) -> ValidationResult:
        """Validate chapter summary takeaways.

        Args:
            takeaways: List of takeaway strings
            min_count: Minimum number of takeaways (default: 3)
            max_count: Maximum number of takeaways (default: 5)

        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []
        metrics = {"takeaway_count": len(takeaways)}

        # Check takeaway count
        if len(takeaways) < min_count:
            errors.append(
                f"Too few takeaways: {len(takeaways)} (minimum {min_count})"
            )
        elif len(takeaways) > max_count:
            errors.append(
                f"Too many takeaways: {len(takeaways)} (maximum {max_count})"
            )

        # Check each takeaway length (50-150 characters per research)
        for i, takeaway in enumerate(takeaways, start=1):
            length = len(takeaway)
            if length < 50:
                errors.append(
                    f"Takeaway {i} too short: {length} chars (minimum 50)"
                )
            elif length > 150:
                warnings.append(
                    f"Takeaway {i} too long: {length} chars (recommended max 150)"
                )

            if not takeaway.strip():
                errors.append(f"Takeaway {i} is empty")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
        )

    def validate_quiz(
        self,
        questions: List[Dict[str, Any]],
        min_questions: int = 5,
        max_questions: int = 7,
    ) -> ValidationResult:
        """Validate quiz questions.

        Args:
            questions: List of question dictionaries with keys:
                - question_text: str
                - options: List[str] (must have 4 options)
                - correct_index: int (0-3)
                - difficulty: str (easy/medium/hard)
            min_questions: Minimum number of questions (default: 5)
            max_questions: Maximum number of questions (default: 7)

        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []
        metrics = {"question_count": len(questions)}

        # Check question count
        if len(questions) < min_questions:
            errors.append(
                f"Too few questions: {len(questions)} (minimum {min_questions})"
            )
        elif len(questions) > max_questions:
            errors.append(
                f"Too many questions: {len(questions)} (maximum {max_questions})"
            )

        # Validate each question
        for i, question in enumerate(questions, start=1):
            # Check required fields
            if "question_text" not in question:
                errors.append(f"Question {i}: missing 'question_text' field")
                continue

            if "options" not in question:
                errors.append(f"Question {i}: missing 'options' field")
                continue

            if "correct_index" not in question:
                errors.append(f"Question {i}: missing 'correct_index' field")
                continue

            # Check options count (must be exactly 4)
            options = question["options"]
            if len(options) != 4:
                errors.append(
                    f"Question {i}: must have exactly 4 options (got {len(options)})"
                )

            # Check correct_index range
            correct_index = question["correct_index"]
            if not (0 <= correct_index <= 3):
                errors.append(
                    f"Question {i}: correct_index must be 0-3 (got {correct_index})"
                )

            # Check for empty question text
            if not question["question_text"].strip():
                errors.append(f"Question {i}: question_text is empty")

            # Check for empty options
            for j, option in enumerate(options):
                if not option.strip():
                    errors.append(f"Question {i}, option {j}: option is empty")

            # Check difficulty if present
            if "difficulty" in question:
                valid_difficulties = ["easy", "medium", "hard"]
                if question["difficulty"] not in valid_difficulties:
                    warnings.append(
                        f"Question {i}: invalid difficulty '{question['difficulty']}' "
                        f"(valid: {valid_difficulties})"
                    )

        # Check for duplicate questions
        question_texts = [q.get("question_text", "") for q in questions]
        if len(question_texts) != len(set(question_texts)):
            warnings.append("Duplicate questions detected")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
        )

    def validate_learning_booster(
        self, content: str, booster_type: str, min_length: int = 100, max_length: int = 300
    ) -> ValidationResult:
        """Validate a learning booster.

        Args:
            content: Booster content text
            booster_type: Type of booster (analogy/example/explanation)
            min_length: Minimum character length (default: 100)
            max_length: Maximum character length (default: 300)

        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []
        length = len(content)
        metrics = {"content_length": length}

        # Check content length
        if length < min_length:
            errors.append(
                f"Booster too short: {length} chars (minimum {min_length})"
            )
        elif length > max_length:
            errors.append(
                f"Booster too long: {length} chars (maximum {max_length})"
            )

        # Check booster type
        valid_types = ["analogy", "example", "explanation"]
        if booster_type not in valid_types:
            errors.append(
                f"Invalid booster type: '{booster_type}' (valid: {valid_types})"
            )

        # Check for empty content
        if not content.strip():
            errors.append("Booster content is empty")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
        )

    # Private helper methods

    def _validate_markdown_syntax(self, content: str) -> List[str]:
        """Validate markdown syntax using markdown-it-py.

        Args:
            content: Markdown content

        Returns:
            List of syntax error messages (empty if valid)
        """
        errors = []
        try:
            # Parse markdown
            tokens = self.md_parser.parse(content)

            # Check for parsing errors (markdown-it is permissive, so manual checks)
            if not tokens:
                errors.append("Failed to parse markdown (empty token list)")

        except Exception as e:
            errors.append(f"Markdown syntax error: {e}")

        return errors

    def _validate_structure(self, content: str) -> List[str]:
        """Validate content structure (headers, sections).

        Args:
            content: Markdown content

        Returns:
            List of structure error messages
        """
        errors = []

        # Check for H1 heading (chapter title)
        h1_pattern = re.compile(r"^#\s+.+$", re.MULTILINE)
        h1_matches = h1_pattern.findall(content)

        if len(h1_matches) == 0:
            errors.append("Missing H1 heading (chapter title)")
        elif len(h1_matches) > 1:
            errors.append(f"Multiple H1 headings found ({len(h1_matches)}), expected 1")

        # Check for at least one H2 section
        h2_pattern = re.compile(r"^##\s+.+$", re.MULTILINE)
        h2_matches = h2_pattern.findall(content)

        if len(h2_matches) == 0:
            errors.append("No H2 sections found (chapter should have sections)")

        return errors

    def _count_words(self, content: str) -> int:
        """Count words in markdown content (excluding code blocks).

        Args:
            content: Markdown content

        Returns:
            Word count
        """
        # Remove code blocks
        content_no_code = re.sub(r"```[\s\S]*?```", "", content)
        content_no_code = re.sub(r"`[^`]+`", "", content_no_code)

        # Remove markdown syntax
        content_no_markdown = re.sub(r"[#*_\[\]()!]", "", content_no_code)

        # Count words
        words = content_no_markdown.split()
        return len(words)

    def _validate_word_count(self, word_count: int) -> List[str]:
        """Validate word count against constitution constraints.

        Args:
            word_count: Word count

        Returns:
            List of error messages
        """
        errors = []

        if word_count < self.MIN_WORD_COUNT:
            errors.append(
                f"Word count too low: {word_count} "
                f"(minimum {self.MIN_WORD_COUNT})"
            )
        elif word_count > self.MAX_WORD_COUNT:
            errors.append(
                f"Word count too high: {word_count} "
                f"(maximum {self.MAX_WORD_COUNT})"
            )

        return errors

    def _calculate_reading_time(self, word_count: int) -> int:
        """Calculate reading time in minutes.

        Args:
            word_count: Word count

        Returns:
            Reading time in minutes (rounded)
        """
        return round(word_count / self.AVERAGE_READING_SPEED)

    def _validate_reading_time(self, reading_time: int) -> List[str]:
        """Validate reading time against constitution constraints.

        Args:
            reading_time: Reading time in minutes

        Returns:
            List of error messages
        """
        errors = []

        if reading_time < self.MIN_READING_TIME:
            errors.append(
                f"Reading time too short: {reading_time} min "
                f"(minimum {self.MIN_READING_TIME})"
            )
        elif reading_time > self.MAX_READING_TIME:
            errors.append(
                f"Reading time too long: {reading_time} min "
                f"(maximum {self.MAX_READING_TIME})"
            )

        return errors

    def _extract_learning_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from chapter content.

        Args:
            content: Markdown content

        Returns:
            List of learning objectives (empty if not found)
        """
        # Look for learning objectives section
        objectives_pattern = re.compile(
            r"##\s*Learning Objectives?\s*\n(.*?)(?=\n##|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        match = objectives_pattern.search(content)

        if not match:
            return []

        objectives_section = match.group(1)

        # Extract list items
        list_items = re.findall(r"^[-*]\s+(.+)$", objectives_section, re.MULTILINE)

        return list_items
