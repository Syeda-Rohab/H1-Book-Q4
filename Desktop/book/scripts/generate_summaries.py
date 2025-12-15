#!/usr/bin/env python3
"""Quick script to generate summaries for all existing chapters.

Usage:
    python scripts/generate_summaries.py
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
from agents.content_generator.summary_generator import SummaryGenerator
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
    """Generate summaries for all existing chapters."""

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY not set. Export it first:")
        logger.error("  export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    logger.info("="*60)
    logger.info("Starting summary generation...")
    logger.info("="*60)

    # Initialize components
    llm_client = LLMClient()
    summary_generator = SummaryGenerator(llm_client=llm_client)
    validator = ContentValidator()
    writer = MarkdownWriter(docs_directory="website/docs")

    # Get MVP curriculum (6 chapters)
    curriculum = get_curriculum(include_extended=False)
    logger.info(f"Generating summaries for {len(curriculum)} chapters\n")

    results = []
    total_tokens = 0

    # Generate summary for each chapter
    for i, chapter_def in enumerate(curriculum, start=1):
        try:
            logger.info(f"{'='*60}")
            logger.info(f"Chapter {i}/{len(curriculum)}: {chapter_def.title}")
            logger.info(f"{'='*60}")

            # Read existing chapter content
            file_path = writer.get_chapter_file_path(
                chapter_def.number,
                chapter_def.slug
            )

            if not file_path.exists():
                logger.warning(f"✗ Chapter file not found: {file_path}")
                logger.warning(f"  Skipping chapter {chapter_def.number}")
                results.append({
                    'chapter': chapter_def.number,
                    'title': chapter_def.title,
                    'status': 'skipped',
                    'reason': 'file not found'
                })
                continue

            # Read chapter content
            chapter_content = file_path.read_text(encoding='utf-8')
            logger.info(f"✓ Read chapter from: {file_path}")

            # Generate summary
            result = summary_generator.generate_summary(
                chapter_content=chapter_content,
                chapter_title=chapter_def.title,
                chapter_number=chapter_def.number
            )

            # Validate summary
            validation = validator.validate_summary(result.takeaways)

            logger.info(f"✓ Generated: {len(result.takeaways)} takeaways, {result.tokens_used} tokens")
            logger.info(f"✓ Valid: {validation.valid} (errors: {len(validation.errors)})")

            if validation.errors:
                for error in validation.errors:
                    logger.warning(f"  - {error}")

            if validation.warnings:
                for warning in validation.warnings:
                    logger.warning(f"  - {warning}")

            # Display takeaways
            logger.info("Takeaways:")
            for j, takeaway in enumerate(result.takeaways, start=1):
                logger.info(f"  {j}. {takeaway} ({len(takeaway)} chars)")

            # Append summary to chapter
            file_info = writer.append_summary_to_chapter(
                chapter_number=chapter_def.number,
                slug=chapter_def.slug,
                takeaways=result.takeaways
            )

            logger.info(f"✓ Summary appended to: {file_info['file_path']}")
            logger.info(f"✓ Takeaways count: {file_info['takeaways_count']}\n")

            total_tokens += result.tokens_used

            results.append({
                'chapter': chapter_def.number,
                'title': chapter_def.title,
                'takeaways': len(result.takeaways),
                'tokens': result.tokens_used,
                'valid': validation.valid,
                'status': 'success'
            })

        except Exception as e:
            logger.error(f"✗ Failed to generate summary for chapter {chapter_def.number}: {e}")
            results.append({
                'chapter': chapter_def.number,
                'title': chapter_def.title,
                'status': 'failed',
                'error': str(e)
            })

    # Print summary
    logger.info("\n" + "="*60)
    logger.info("SUMMARY GENERATION COMPLETE")
    logger.info("="*60)

    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    skipped = sum(1 for r in results if r.get('status') == 'skipped')

    logger.info(f"\nTotal chapters: {len(results)}")
    logger.info(f"Successful: {successful}/{len(results)}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"Total tokens: {total_tokens:,}")

    # Estimate cost (Haiku pricing: $0.25 per million input tokens, $1.25 per million output tokens)
    # Rough estimate assuming 50/50 split
    estimated_cost = (total_tokens / 1_000_000) * 0.75
    logger.info(f"Estimated cost: ${estimated_cost:.4f}")

    if successful == len(results):
        logger.info("\n✅ All summaries generated successfully!")
        logger.info("\nNext steps:")
        logger.info("  1. cd website")
        logger.info("  2. npm run start  # Preview locally")
        logger.info("  3. Check summary sections at the end of each chapter")
    elif failed > 0:
        logger.error(f"\n❌ {failed} summaries failed to generate")
        logger.info("\nCheck the logs above for details")
        sys.exit(1)
    else:
        logger.warning(f"\n⚠️  {skipped} chapters skipped (files not found)")
        logger.info("\nGenerate chapters first using:")
        logger.info("  python scripts/generate_chapters.py")


if __name__ == "__main__":
    main()
