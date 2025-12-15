#!/usr/bin/env python3
"""Generate a single chapter quickly.

Usage:
    python scripts/generate_single.py 1  # Generate chapter 1
"""

import os
import sys
import logging
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.content_generator.curriculum import get_chapter_by_number
from agents.content_generator.chapter_generator import ChapterGenerator
from agents.content_generator.validator import ContentValidator
from agents.content_generator.markdown_writer import MarkdownWriter

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_single.py <chapter_number>")
        sys.exit(1)

    chapter_num = int(sys.argv[1])

    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("Set ANTHROPIC_API_KEY first")
        sys.exit(1)

    # Get chapter definition
    chapter_def = get_chapter_by_number(chapter_num)
    logger.info(f"Generating: {chapter_def.title}")

    # Generate
    generator = ChapterGenerator()
    result = generator.generate_chapter(chapter_def)

    # Validate
    validator = ContentValidator()
    validation = validator.validate_chapter(result.content)

    # Write
    writer = MarkdownWriter(docs_directory="website/docs")
    file_info = writer.write_chapter(
        chapter_number=chapter_def.number,
        title=chapter_def.title,
        slug=chapter_def.slug,
        content=result.content
    )

    # Report
    logger.info(f"✓ Words: {result.word_count}")
    logger.info(f"✓ Tokens: {result.tokens_used}")
    logger.info(f"✓ Valid: {validation.valid}")
    logger.info(f"✓ File: {file_info['file_path']}")

    if validation.errors:
        logger.warning("Validation errors:")
        for err in validation.errors:
            logger.warning(f"  - {err}")


if __name__ == "__main__":
    main()
