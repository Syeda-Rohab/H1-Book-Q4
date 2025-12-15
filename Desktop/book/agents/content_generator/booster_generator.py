"""Learning booster generation (T057)."""
import json, logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from agents.content_generator.llm_client import LLMClient, GenerationError
from agents.content_generator.prompts import BOOSTER_GENERATION_SYSTEM_PROMPT, get_booster_generation_prompt
from agents.content_generator.validator import ContentValidator
logger = logging.getLogger(__name__)

@dataclass
class BoosterGenerationResult:
    boosters: List[Dict[str, Any]]
    chapter_number: int
    chapter_title: str
    tokens_used: int
    model_used: str
    generation_attempts: int
    validation_passed: bool

class BoosterGenerator:
    """Generates learning boosters (analogies, examples, explanations)."""
    def __init__(self, llm_client: Optional[LLMClient] = None, validator: Optional[ContentValidator] = None, max_attempts: int = 3, num_boosters: int = 3):
        self.llm_client = llm_client or LLMClient()
        self.validator = validator or ContentValidator()
        self.max_attempts = max_attempts
        self.num_boosters = max(2, min(3, num_boosters))
        logger.info(f"BoosterGenerator initialized (num_boosters={self.num_boosters})")

    def generate_boosters(self, chapter_content: str, chapter_title: str, chapter_number: int) -> BoosterGenerationResult:
        """Generate 2-3 learning boosters for a chapter."""
        logger.info(f"Starting booster generation for Chapter {chapter_number}")
        model = LLMClient.get_model_for_task("booster")
        for attempt in range(1, self.max_attempts + 1):
            try:
                logger.info(f"Booster attempt {attempt}/{self.max_attempts} for Chapter {chapter_number}")
                sections = self._extract_sections(chapter_content)
                section_text = sections[0] if sections else chapter_content[:1000]
                user_prompt = get_booster_generation_prompt(chapter_content, chapter_title, section_text, "analogy", self.num_boosters)
                result = self.llm_client.generate_with_rate_limit_buffer(prompt=user_prompt, system_prompt=BOOSTER_GENERATION_SYSTEM_PROMPT, model=model, max_tokens=1024, temperature=1.0)
                boosters = self._parse_boosters_json(result.content.strip())
                logger.info(f"Chapter {chapter_number} boosters parsed: {len(boosters)} boosters ({result.tokens_used} tokens)")
                all_valid = all(self.validator.validate_learning_booster(b['content'], b['booster_type']).valid for b in boosters)
                return BoosterGenerationResult(boosters=boosters, chapter_number=chapter_number, chapter_title=chapter_title, tokens_used=result.tokens_used, model_used=result.model, generation_attempts=attempt, validation_passed=all_valid)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse booster JSON on attempt {attempt}: {e}")
                if attempt >= self.max_attempts:
                    raise GenerationError(f"Failed to parse booster JSON after {self.max_attempts} attempts") from e
            except GenerationError as e:
                logger.error(f"Generation error on attempt {attempt} for Chapter {chapter_number}: {e}")
                if attempt >= self.max_attempts:
                    raise
        raise GenerationError(f"Failed to generate boosters for Chapter {chapter_number} after {self.max_attempts} attempts")

    def _extract_sections(self, content: str) -> List[str]:
        """Extract H2 sections from chapter."""
        import re
        sections = re.split(r'\n##\s+', content)
        return [s.strip() for s in sections if s.strip()]

    def _parse_boosters_json(self, content: str) -> List[Dict[str, Any]]:
        """Parse JSON array of boosters."""
        content = content.strip()
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content[3:]
        if content.endswith("```"): content = content[:-3]
        parsed = json.loads(content.strip())
        if not isinstance(parsed, list): raise ValueError(f"Expected array, got {type(parsed)}")
        return parsed

    def get_total_tokens_used(self) -> int:
        return self.llm_client.get_total_tokens_used()
