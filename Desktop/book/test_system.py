#!/usr/bin/env python3
"""Test the chapter generation system without API key."""
import sys
sys.path.insert(0, '.')

from agents.content_generator.curriculum import get_curriculum
from agents.content_generator.prompts import get_chapter_generation_prompt

print("="*60)
print("CHAPTER GENERATION SYSTEM - READY FOR USE")
print("="*60)
print()

# Test curriculum
curriculum = get_curriculum(include_extended=False)
print(f"[OK] Curriculum loaded: {len(curriculum)} MVP chapters")

# Show chapters
print("\nChapters to be generated:")
for ch in curriculum:
    print(f"  {ch.number}. {ch.title}")
    print(f"     - Target: {ch.word_count_target} words")
    print(f"     - Topics: {len(ch.topics)}")
    print(f"     - Objectives: {len(ch.learning_objectives)}")

# Test prompt generation
print("\n[OK] Prompt generation system working")
prompt = get_chapter_generation_prompt(curriculum[0])
print(f"     Sample prompt length: {len(prompt)} chars")

print("\n" + "="*60)
print("SYSTEM STATUS: READY")
print("="*60)
print("\nTo generate chapters:")
print("  1. export ANTHROPIC_API_KEY='your-key'")
print("  2. PYTHONPATH=. python scripts/generate_single.py 1")
print()
