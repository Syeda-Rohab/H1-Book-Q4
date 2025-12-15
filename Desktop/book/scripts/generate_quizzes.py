#!/usr/bin/env python3
"""Generate quizzes for all chapters."""
import os, sys, logging
from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
load_dotenv(project_root / ".env")
from agents.content_generator.curriculum import get_curriculum
from agents.content_generator.quiz_generator import QuizGenerator
from agents.content_generator.markdown_writer import MarkdownWriter
from agents.content_generator.llm_client import LLMClient
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    if not os.getenv("ANTHROPIC_API_KEY"): logger.error("ANTHROPIC_API_KEY not set"); sys.exit(1)
    logger.info("Starting quiz generation")
    llm = LLMClient(); quiz_gen = QuizGenerator(llm, num_questions=5); writer = MarkdownWriter("website/docs")
    curriculum = get_curriculum(False); results = []; tokens = 0
    for i, ch in enumerate(curriculum, 1):
        try:
            logger.info(f"Chapter {i}/{len(curriculum)}: {ch.title}")
            path = writer.get_chapter_file_path(ch.number, ch.slug)
            if not path.exists(): logger.warning(f"Skip {ch.number}"); continue
            content = path.read_text('utf-8')
            result = quiz_gen.generate_quiz(content, ch.title, ch.number)
            writer.append_quiz_to_chapter(ch.number, ch.slug, result.questions)
            logger.info(f"✓ {len(result.questions)} questions, {result.tokens_used} tokens")
            tokens += result.tokens_used; results.append('success')
        except Exception as e: logger.error(f"✗ {e}"); results.append('failed')
    logger.info(f"Complete: {results.count('success')}/{len(results)}, {tokens} tokens")

if __name__ == "__main__": main()
