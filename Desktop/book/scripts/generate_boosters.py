#!/usr/bin/env python3
"""Generate learning boosters (T062)."""
import os, sys, logging
from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
load_dotenv(project_root / ".env")
from agents.content_generator.curriculum import get_curriculum
from agents.content_generator.booster_generator import BoosterGenerator
from agents.content_generator.markdown_writer import MarkdownWriter
from agents.content_generator.llm_client import LLMClient
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    if not os.getenv("ANTHROPIC_API_KEY"): logger.error("API key not set"); sys.exit(1)
    logger.info("Starting booster generation")
    llm = LLMClient(); gen = BoosterGenerator(llm, num_boosters=3); writer = MarkdownWriter("website/docs")
    curriculum = get_curriculum(False); results = []; tokens = 0
    for i, ch in enumerate(curriculum, 1):
        try:
            logger.info(f"Chapter {i}/{len(curriculum)}: {ch.title}")
            path = writer.get_chapter_file_path(ch.number, ch.slug)
            if not path.exists(): logger.warning(f"Skip {ch.number}"); continue
            content = path.read_text('utf-8')
            result = gen.generate_boosters(content, ch.title, ch.number)
            writer.embed_boosters_in_chapter(ch.number, ch.slug, result.boosters)
            logger.info(f"✓ {len(result.boosters)} boosters, {result.tokens_used} tokens")
            tokens += result.tokens_used; results.append('success')
        except Exception as e: logger.error(f"✗ {e}"); results.append('failed')
    logger.info(f"Complete: {results.count('success')}/{len(results)}, {tokens} tokens")

if __name__ == "__main__": main()
