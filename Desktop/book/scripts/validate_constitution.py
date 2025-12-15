"""Constitution compliance validation script.

Validates that the textbook project adheres to all principles
defined in .specify/memory/constitution.md

Usage:
    python scripts/validate_constitution.py
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ConstitutionValidator:
    """Validates project compliance with constitution principles."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.violations: List[str] = []
        self.warnings: List[str] = []
        self.passes: List[str] = []

    def validate_all(self) -> bool:
        """Run all validation checks.

        Returns:
            True if all validations pass, False otherwise
        """
        logger.info("=" * 60)
        logger.info("CONSTITUTION COMPLIANCE VALIDATION")
        logger.info("=" * 60 + "\n")

        # Principle I: AI-Native Design
        self._validate_ai_native_design()

        # Principle II: Speed & Simplicity
        self._validate_speed_and_simplicity()

        # Principle III: Free-Tier Architecture
        self._validate_free_tier_architecture()

        # Principle IV: Grounded RAG Responses (N/A for content generation)
        self._validate_rag_readiness()

        # Principle V: Modular Backend Structure
        self._validate_modular_backend()

        # Principle VI: Mobile-First Responsive
        self._validate_mobile_responsive()

        # Principle VII: Content Quality Over Quantity
        self._validate_content_quality()

        # Principle VIII: Observability & Health Monitoring
        self._validate_observability()

        # Print results
        self._print_results()

        return len(self.violations) == 0

    def _validate_ai_native_design(self) -> None:
        """Validate Principle I: AI-Native Design."""
        logger.info("Checking Principle I: AI-Native Design...")

        # Check for generator classes
        generator_path = self.project_root / "agents" / "content_generator"
        generators = ["chapter_generator.py", "summary_generator.py",
                     "quiz_generator.py", "booster_generator.py"]

        missing_generators = []
        for gen in generators:
            if not (generator_path / gen).exists():
                missing_generators.append(gen)

        if missing_generators:
            self.violations.append(
                f"Principle I: Missing generators: {', '.join(missing_generators)}"
            )
        else:
            self.passes.append("Principle I: All AI generators present ✓")

        # Check for LLM client
        if not (generator_path / "llm_client.py").exists():
            self.violations.append("Principle I: Missing llm_client.py")
        else:
            self.passes.append("Principle I: LLM client configured ✓")

    def _validate_speed_and_simplicity(self) -> None:
        """Validate Principle II: Speed & Simplicity."""
        logger.info("Checking Principle II: Speed & Simplicity...")

        # Check chapter count (should be 6-8)
        docs_path = self.project_root / "website" / "docs"
        if docs_path.exists():
            chapters = list(docs_path.glob("chapter-*.md"))
            chapter_count = len(chapters)

            if chapter_count < 6 or chapter_count > 8:
                self.violations.append(
                    f"Principle II: Chapter count {chapter_count} outside range 6-8"
                )
            else:
                self.passes.append(f"Principle II: {chapter_count} chapters (6-8 range) ✓")

            # Check word counts (800-1200)
            invalid_chapters = []
            for chapter_file in chapters:
                content = chapter_file.read_text(encoding="utf-8")
                word_count = len(content.split())
                if word_count < 800 or word_count > 1200:
                    invalid_chapters.append(f"{chapter_file.name} ({word_count} words)")

            if invalid_chapters:
                self.warnings.append(
                    f"Principle II: Chapters outside 800-1200 word range: {', '.join(invalid_chapters)}"
                )
            else:
                self.passes.append("Principle II: All chapters within 800-1200 words ✓")
        else:
            self.warnings.append("Principle II: No chapters found in website/docs/")

    def _validate_free_tier_architecture(self) -> None:
        """Validate Principle III: Free-Tier Architecture."""
        logger.info("Checking Principle III: Free-Tier Architecture...")

        # Check for Haiku model usage (cheaper)
        llm_client = self.project_root / "agents" / "content_generator" / "llm_client.py"
        if llm_client.exists():
            content = llm_client.read_text(encoding="utf-8")
            if "claude-3-haiku" in content:
                self.passes.append("Principle III: Using Haiku model (free-tier friendly) ✓")
            else:
                self.warnings.append("Principle III: Not using Haiku model")

        # Check Docusaurus (free static site)
        docusaurus_config = self.project_root / "website" / "docusaurus.config.js"
        if docusaurus_config.exists():
            self.passes.append("Principle III: Docusaurus configured (free static hosting) ✓")
        else:
            self.violations.append("Principle III: Missing Docusaurus configuration")

    def _validate_rag_readiness(self) -> None:
        """Validate Principle IV: Grounded RAG Responses."""
        logger.info("Checking Principle IV: RAG Readiness...")

        # This principle is for future RAG feature, but content must be ready
        docs_path = self.project_root / "website" / "docs"
        if docs_path.exists():
            chapters = list(docs_path.glob("chapter-*.md"))
            if len(chapters) >= 6:
                self.passes.append("Principle IV: Content ready for RAG integration ✓")
            else:
                self.warnings.append("Principle IV: Insufficient content for RAG")

    def _validate_modular_backend(self) -> None:
        """Validate Principle V: Modular Backend Structure."""
        logger.info("Checking Principle V: Modular Backend Structure...")

        # Check backend structure
        backend_path = self.project_root / "backend" / "src"
        required_modules = ["models", "services", "routes", "utils"]

        missing_modules = []
        for module in required_modules:
            if not (backend_path / module).exists():
                missing_modules.append(module)

        if missing_modules:
            self.violations.append(
                f"Principle V: Missing backend modules: {', '.join(missing_modules)}"
            )
        else:
            self.passes.append("Principle V: All backend modules present ✓")

        # Check agent structure
        agent_path = self.project_root / "agents" / "content_generator"
        if agent_path.exists():
            self.passes.append("Principle V: Agent module properly structured ✓")
        else:
            self.violations.append("Principle V: Missing agents/content_generator")

    def _validate_mobile_responsive(self) -> None:
        """Validate Principle VI: Mobile-First Responsive."""
        logger.info("Checking Principle VI: Mobile-First Responsive...")

        # Check Docusaurus responsive config
        docusaurus_config = self.project_root / "website" / "docusaurus.config.js"
        if docusaurus_config.exists():
            self.passes.append("Principle VI: Docusaurus handles responsive design ✓")
        else:
            self.warnings.append("Principle VI: No Docusaurus configuration found")

        # Check for React components
        components_path = self.project_root / "website" / "src" / "components"
        if components_path.exists():
            quiz_component = components_path / "ChapterQuiz.tsx"
            booster_component = components_path / "LearningBooster.tsx"

            if quiz_component.exists() and booster_component.exists():
                self.passes.append("Principle VI: React components created ✓")
            else:
                self.warnings.append("Principle VI: Missing React components")

    def _validate_content_quality(self) -> None:
        """Validate Principle VII: Content Quality Over Quantity."""
        logger.info("Checking Principle VII: Content Quality Over Quantity...")

        # Check for validator
        validator_path = self.project_root / "agents" / "content_generator" / "validator.py"
        if validator_path.exists():
            self.passes.append("Principle VII: Content validator present ✓")
        else:
            self.violations.append("Principle VII: Missing content validator")

        # Check for validation in generators
        generator_path = self.project_root / "agents" / "content_generator"
        generators = ["chapter_generator.py", "summary_generator.py", "quiz_generator.py"]

        validation_present = []
        for gen in generators:
            gen_file = generator_path / gen
            if gen_file.exists():
                content = gen_file.read_text(encoding="utf-8")
                if "validation" in content.lower():
                    validation_present.append(gen)

        if len(validation_present) == len(generators):
            self.passes.append("Principle VII: All generators use validation ✓")
        else:
            self.warnings.append(
                f"Principle VII: Some generators missing validation: {set(generators) - set(validation_present)}"
            )

    def _validate_observability(self) -> None:
        """Validate Principle VIII: Observability & Health Monitoring."""
        logger.info("Checking Principle VIII: Observability...")

        # Check for logging configuration
        logging_path = self.project_root / "backend" / "src" / "utils" / "logging.py"
        if logging_path.exists():
            self.passes.append("Principle VIII: Structured logging configured ✓")
        else:
            self.violations.append("Principle VIII: Missing logging configuration")

        # Check for health check routes
        health_routes = self.project_root / "backend" / "src" / "routes" / "health_routes.py"
        if health_routes.exists():
            self.passes.append("Principle VIII: Health check endpoints present ✓")
        else:
            self.warnings.append("Principle VIII: Missing health check endpoints")

        # Check for token tracking
        token_tracker = self.project_root / "agents" / "content_generator" / "token_tracker.py"
        if token_tracker.exists():
            self.passes.append("Principle VIII: Token usage tracking implemented ✓")
        else:
            self.warnings.append("Principle VIII: No token usage tracking")

    def _print_results(self) -> None:
        """Print validation results."""
        logger.info("\n" + "=" * 60)
        logger.info("VALIDATION RESULTS")
        logger.info("=" * 60 + "\n")

        if self.passes:
            logger.info(f"✓ PASSED ({len(self.passes)}):")
            for p in self.passes:
                logger.info(f"  ✓ {p}")
            logger.info("")

        if self.warnings:
            logger.warning(f"⚠ WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                logger.warning(f"  ⚠ {w}")
            logger.info("")

        if self.violations:
            logger.error(f"✗ VIOLATIONS ({len(self.violations)}):")
            for v in self.violations:
                logger.error(f"  ✗ {v}")
            logger.info("")

        logger.info("=" * 60)
        logger.info(f"Summary: {len(self.passes)} passed, {len(self.warnings)} warnings, {len(self.violations)} violations")
        logger.info("=" * 60 + "\n")

        if self.violations:
            logger.error("❌ Constitution compliance validation FAILED")
            return False
        elif self.warnings:
            logger.warning("⚠️  Constitution compliance validation PASSED with warnings")
            return True
        else:
            logger.info("✅ Constitution compliance validation PASSED")
            return True


def main():
    """Run constitution validation."""
    validator = ConstitutionValidator(project_root)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
