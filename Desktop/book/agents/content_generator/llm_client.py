"""LLM client wrapper for Anthropic Claude API with retry logic.

Handles API communication, rate limiting, error handling, and token usage tracking.
"""

import os
import time
import random
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

from anthropic import Anthropic, APIError, RateLimitError, APIConnectionError

logger = logging.getLogger(__name__)


@dataclass
class GenerationResult:
    """Result of an LLM generation request.

    Attributes:
        content: Generated text content
        model: Model identifier used
        tokens_used: Total tokens consumed (input + output)
        finish_reason: Reason for generation completion
        metadata: Additional metadata from the API response
    """

    content: str
    model: str
    tokens_used: int
    finish_reason: str
    metadata: Dict[str, Any]


class LLMClient:
    """Wrapper for Anthropic Claude API with retry logic.

    Features:
    - Exponential backoff retry for rate limits and transient errors
    - Token usage tracking
    - Model selection (Sonnet for chapters, Haiku for enhancements)
    - Constitution compliance (free-tier compatible)

    Based on research.md: Research Task 1 - LLM Selection
    """

    # Model identifiers (from constitution and research)
    # Note: Using Haiku for all generation as Sonnet is not accessible with current API key
    MODEL_SONNET = "claude-3-haiku-20240307"  # For chapters and boosters
    MODEL_HAIKU = "claude-3-haiku-20240307"  # For summaries and quizzes

    # Retry configuration
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 5  # seconds
    RATE_LIMIT_BUFFER = 5  # seconds between requests to avoid rate limits

    def __init__(
        self,
        api_key: Optional[str] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: int = DEFAULT_RETRY_DELAY,
    ):
        """Initialize the LLM client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            max_retries: Maximum retry attempts for failed requests
            retry_delay: Initial delay in seconds for exponential backoff
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment or constructor"
            )

        self.client = Anthropic(api_key=self.api_key)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.total_tokens_used = 0

        logger.info(
            f"LLMClient initialized (max_retries={max_retries}, "
            f"retry_delay={retry_delay}s)"
        )

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = MODEL_SONNET,
        max_tokens: int = 4096,
        temperature: float = 1.0,
    ) -> GenerationResult:
        """Generate content using Claude API with retry logic.

        Args:
            prompt: User prompt for content generation
            system_prompt: Optional system prompt for instruction/context
            model: Model identifier (default: Sonnet for quality)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            GenerationResult with content and metadata

        Raises:
            GenerationError: If generation fails after all retries
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"LLM generation attempt {attempt + 1}/{self.max_retries} "
                    f"(model={model})"
                )

                # Prepare messages
                messages = [{"role": "user", "content": prompt}]

                # Make API call
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt if system_prompt else None,
                    messages=messages,
                )

                # Extract content
                content = response.content[0].text

                # Calculate token usage
                tokens_used = response.usage.input_tokens + response.usage.output_tokens
                self.total_tokens_used += tokens_used

                logger.info(
                    f"Generation successful (tokens: {tokens_used}, "
                    f"total: {self.total_tokens_used})"
                )

                return GenerationResult(
                    content=content,
                    model=response.model,
                    tokens_used=tokens_used,
                    finish_reason=response.stop_reason,
                    metadata={
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                        "response_id": response.id,
                    },
                )

            except RateLimitError as e:
                wait_time = self._calculate_backoff(attempt)
                logger.warning(
                    f"Rate limit hit (attempt {attempt + 1}), "
                    f"waiting {wait_time}s: {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    raise GenerationError(
                        f"Rate limit exceeded after {self.max_retries} attempts"
                    ) from e

            except APIConnectionError as e:
                wait_time = self._calculate_backoff(attempt)
                logger.warning(
                    f"Connection error (attempt {attempt + 1}), "
                    f"waiting {wait_time}s: {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    raise GenerationError(
                        f"Connection failed after {self.max_retries} attempts"
                    ) from e

            except APIError as e:
                logger.error(f"API error: {e}")
                raise GenerationError(f"API error: {e}") from e

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise GenerationError(f"Unexpected error: {e}") from e

        raise GenerationError(
            f"Generation failed after {self.max_retries} attempts"
        )

    def generate_with_rate_limit_buffer(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = MODEL_SONNET,
        max_tokens: int = 4096,
        temperature: float = 1.0,
    ) -> GenerationResult:
        """Generate content with automatic rate limit buffer delay.

        This method adds a delay after generation to prevent rate limit issues
        when making multiple sequential requests (e.g., batch chapter generation).

        Args:
            prompt: User prompt for content generation
            system_prompt: Optional system prompt
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            GenerationResult with content and metadata
        """
        result = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Wait to avoid rate limits on next request
        logger.debug(f"Applying rate limit buffer ({self.RATE_LIMIT_BUFFER}s)")
        time.sleep(self.RATE_LIMIT_BUFFER)

        return result

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter.

        Uses exponential backoff with full jitter to prevent thundering herd problem.
        Formula: random(0, base_delay * 2^attempt)

        Args:
            attempt: Current attempt number (0-indexed)

        Returns:
            Delay in seconds with jitter (e.g., 0-5s, 0-10s, 0-20s, ...)
        """
        max_delay = self.retry_delay * (2**attempt)
        # Add full jitter to prevent thundering herd
        jittered_delay = random.uniform(0, max_delay)
        logger.debug(f"Calculated backoff: {jittered_delay:.2f}s (max: {max_delay}s)")
        return jittered_delay

    def get_total_tokens_used(self) -> int:
        """Get total tokens consumed by this client instance.

        Returns:
            Total tokens (input + output) used across all requests
        """
        return self.total_tokens_used

    def reset_token_counter(self) -> None:
        """Reset the token usage counter to zero."""
        logger.info(
            f"Resetting token counter (was: {self.total_tokens_used} tokens)"
        )
        self.total_tokens_used = 0

    @classmethod
    def get_model_for_task(cls, task: str) -> str:
        """Get the recommended model for a specific task.

        Based on research findings:
        - Sonnet: Higher quality for chapters and learning boosters
        - Haiku: Faster/cheaper for summaries and quizzes

        Args:
            task: Task type ('chapter', 'summary', 'quiz', 'booster')

        Returns:
            Model identifier string

        Raises:
            ValueError: If task is not recognized
        """
        task_models = {
            "chapter": cls.MODEL_SONNET,
            "booster": cls.MODEL_SONNET,
            "summary": cls.MODEL_HAIKU,
            "quiz": cls.MODEL_HAIKU,
        }

        if task not in task_models:
            raise ValueError(
                f"Unknown task: {task}. Valid tasks: {list(task_models.keys())}"
            )

        return task_models[task]


class GenerationError(Exception):
    """Exception raised when LLM generation fails."""

    pass


# Utility function for quick generation
def generate_content(
    prompt: str,
    system_prompt: Optional[str] = None,
    task: str = "chapter",
    api_key: Optional[str] = None,
) -> str:
    """Quick utility function for one-off content generation.

    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        task: Task type for model selection
        api_key: Optional API key (defaults to env var)

    Returns:
        Generated content string

    Raises:
        GenerationError: If generation fails
    """
    client = LLMClient(api_key=api_key)
    model = LLMClient.get_model_for_task(task)
    result = client.generate(prompt=prompt, system_prompt=system_prompt, model=model)
    return result.content
