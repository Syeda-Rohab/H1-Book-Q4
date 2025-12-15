# Quick Start Guide - Chapter Generation

## Phase 3 Implementation Complete! ✅

All infrastructure is ready for generating 6 MVP chapters on Physical AI & Humanoid Robotics.

## Prerequisites

✅ Dependencies installed: `anthropic`, `markdown-it-py`
⚠️ **Required**: Set your Anthropic API key

## Generate Chapters

### Option 1: Single Chapter (Fast Test)

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Generate Chapter 1 only
cd /c/Users/Dell/Desktop/book
PYTHONPATH=. python scripts/generate_single.py 1
```

**Expected output**: Chapter written to `website/docs/chapter-01-physical-ai-intro.md`

### Option 2: All 6 MVP Chapters (Full Run)

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Generate all chapters (~10-15 minutes)
PYTHONPATH=. python scripts/generate_chapters.py
```

**Expected output**:
- Chapter 1: Introduction to Physical AI
- Chapter 2: Humanoid Robotics Fundamentals
- Chapter 3: Sensors and Perception
- Chapter 4: Actuators and Motion
- Chapter 5: AI for Robot Control
- Chapter 6: Manipulation and Dexterity

**Estimated time**: 10-15 minutes (with 5s delays between chapters)
**Estimated tokens**: ~40,000 tokens total

## Preview Generated Content

```bash
cd website
npm install  # If not done yet
npm run start
```

Open: http://localhost:3000/docs/intro

## Validation Checks

Each chapter automatically validates:
- ✅ Word count: 800-1200 words
- ✅ Reading time: 5-7 minutes
- ✅ Markdown syntax
- ✅ Learning objectives present
- ✅ Proper heading structure (H1, H2)

## Architecture Overview

```
agents/content_generator/
├── curriculum.py         # 6 chapter definitions
├── chapter_generator.py  # AI generation logic
├── prompts.py           # System prompts
├── validator.py         # Content validation
├── llm_client.py        # Anthropic API wrapper
└── markdown_writer.py   # Docusaurus file writer

scripts/
├── generate_single.py   # Generate one chapter
└── generate_chapters.py # Generate all chapters

website/docs/
├── intro.md            # Textbook homepage (✅ created)
└── chapter-*.md        # Generated chapters (⏳ pending)
```

## Constitution Compliance

- **Principle II**: Speed & Simplicity (6 chapters, 800-1200 words each) ✅
- **Principle III**: Free-Tier Architecture (Anthropic API with rate limits) ✅
- **Principle VII**: Content Quality Over Quantity (strict word limits) ✅
- **Principle VIII**: Observability (token tracking, validation logging) ✅

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'anthropic'`
**Fix**: `pip install anthropic markdown-it-py`

**Issue**: `ANTHROPIC_API_KEY not set`
**Fix**: `export ANTHROPIC_API_KEY="your-key"`

**Issue**: Rate limit errors
**Fix**: Generation has 5s delays between chapters automatically

## Next Steps After Generation

1. **Validate**: Check `website/docs/` for generated markdown files
2. **Preview**: `cd website && npm run start`
3. **Build**: `cd website && npm run build`
4. **Test Mobile**: Open on device, verify <3s load time
5. **Phase 4**: Implement chapter summaries (User Story 2)

---

**Status**: Phase 3 (T022-T032) Complete ✅
**Next**: T033-T037 (Actual generation - requires API key)
