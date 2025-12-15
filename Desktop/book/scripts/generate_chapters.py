#!/usr/bin/env python3
"""Quick script to generate all MVP chapters.

Usage:
    python scripts/generate_chapters.py
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
load_dotenv(project_root / ".env")

from agents.content_generator.curriculum import get_curriculum
from agents.content_generator.chapter_generator import ChapterGenerator
from agents.content_generator.validator import ContentValidator
from agents.content_generator.markdown_writer import MarkdownWriter
from agents.content_generator.llm_client import LLMClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Generate all MVP chapters."""

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY not set. Export it first:")
        logger.error("  export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    logger.info("Starting chapter generation...")

    # Initialize components
    llm_client = LLMClient()
    generator = ChapterGenerator(llm_client=llm_client)
    validator = ContentValidator()
    writer = MarkdownWriter(docs_directory="website/docs")

    # Get MVP curriculum (6 chapters)
    curriculum = get_curriculum(include_extended=False)
    logger.info(f"Generating {len(curriculum)} MVP chapters")

    results = []

    # Generate each chapter
    for i, chapter_def in enumerate(curriculum, start=1):
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Chapter {i}/{len(curriculum)}: {chapter_def.title}")
            logger.info(f"{'='*60}\n")

            # Generate
            result = generator.generate_chapter(chapter_def)

            # Validate
            validation = validator.validate_chapter(result.content)

            logger.info(f"✓ Generated: {result.word_count} words, {result.tokens_used} tokens")
            logger.info(f"✓ Valid: {validation.valid} (errors: {len(validation.errors)})")

            if validation.errors:
                for error in validation.errors:
                    logger.warning(f"  - {error}")

            # Write markdown
            file_info = writer.write_chapter(
                chapter_number=chapter_def.number,
                title=chapter_def.title,
                slug=chapter_def.slug,
                content=result.content
            )

            logger.info(f"✓ Written to: {file_info['file_path']}")
            logger.info(f"✓ URL: {file_info['docusaurus_url']}")

            results.append({
                'chapter': chapter_def.number,
                'title': chapter_def.title,
                'words': result.word_count,
                'tokens': result.tokens_used,
                'valid': validation.valid,
                'file': file_info['file_path']
            })

        except Exception as e:
            logger.error(f"✗ Failed to generate chapter {chapter_def.number}: {e}")
            results.append({
                'chapter': chapter_def.number,
                'title': chapter_def.title,
                'error': str(e)
            })

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("GENERATION COMPLETE")
    logger.info(f"{'='*60}\n")

    total_tokens = sum(r.get('tokens', 0) for r in results)
    successful = sum(1 for r in results if r.get('valid'))

    logger.info(f"Total chapters: {len(results)}")
    logger.info(f"Successful: {successful}/{len(results)}")
    logger.info(f"Total tokens: {total_tokens}")

    for r in results:
        status = "✓" if r.get('valid') else "✗"
        logger.info(f"  {status} Chapter {r['chapter']}: {r['title']}")

    logger.info("\nNext steps:")
    logger.info("  1. cd website")
    logger.info("  2. npm run start  # Test locally")
    logger.info("  3. npm run build  # Production build")


if __name__ == "__main__":
    main()
