# 🚀 Generate All Chapters NOW

## System is 100% Ready! ✅

Everything is implemented and tested. Follow these steps to generate all 6 chapters.

## Step 1: Set Your API Key

```bash
# In your terminal, export your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-YOUR-API-KEY-here"

# Verify it's set
echo $ANTHROPIC_API_KEY
```

## Step 2: Generate Chapters

### Option A: Generate All 6 Chapters (Recommended)

```bash
cd /c/Users/Dell/Desktop/book
PYTHONPATH=. python scripts/generate_chapters.py
```

**Time**: ~10-15 minutes
**Output**: All 6 chapters in `website/docs/`
**Tokens**: ~40,000 tokens (~$0.12 with Sonnet pricing)

### Option B: Generate One at a Time

```bash
cd /c/Users/Dell/Desktop/book

# Chapter 1: Introduction to Physical AI
PYTHONPATH=. python scripts/generate_single.py 1

# Chapter 2: Humanoid Robotics Fundamentals
PYTHONPATH=. python scripts/generate_single.py 2

# Chapter 3: Sensors and Perception
PYTHONPATH=. python scripts/generate_single.py 3

# Chapter 4: Actuators and Motion
PYTHONPATH=. python scripts/generate_single.py 4

# Chapter 5: AI for Robot Control
PYTHONPATH=. python scripts/generate_single.py 5

# Chapter 6: Manipulation and Dexterity
PYTHONPATH=. python scripts/generate_single.py 6
```

## Step 3: Preview Your Textbook

```bash
cd website
npm install  # First time only
npm run start
```

Open: **http://localhost:3000/docs/intro**

## What Gets Generated

Each chapter will be:
- ✅ 800-1200 words (constitution-compliant)
- ✅ 5-7 minute read time
- ✅ Proper markdown with frontmatter
- ✅ Learning objectives section
- ✅ Well-structured with H2 sections
- ✅ Validated automatically

### Files Created

```
website/docs/
├── intro.md                           # ✅ Already created
├── chapter-01-physical-ai-intro.md    # ✅ Sample created
├── chapter-02-humanoid-robotics-fundamentals.md
├── chapter-03-sensors-perception.md
├── chapter-04-actuators-motion.md
├── chapter-05-ai-robot-control.md
└── chapter-06-manipulation-dexterity.md
```

## Expected Console Output

```
============================================================
Starting chapter generation...
Generating 6 MVP chapters
============================================================

Chapter 1/6: Introduction to Physical AI
✓ Generated: 1043 words, 3421 tokens
✓ Valid: True (errors: 0)
✓ Written to: website/docs/chapter-01-physical-ai-intro.md
✓ URL: /docs/physical-ai-intro

[5 second delay...]

Chapter 2/6: Humanoid Robotics Fundamentals
...

============================================================
GENERATION COMPLETE
============================================================

Total chapters: 6
Successful: 6/6
Total tokens: 42,156

Next steps:
  1. cd website
  2. npm run start  # Test locally
  3. npm run build  # Production build
```

## Validation

Each chapter is automatically validated for:
- Word count: 800-1200 ✅
- Reading time: 5-7 minutes ✅
- Markdown syntax ✅
- H1 heading present ✅
- H2 sections present ✅
- Learning objectives included ✅

## Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip install anthropic markdown-it-py
```

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Rate limit errors
The script has built-in 5-second delays. If you still hit limits, increase delay in:
`agents/content_generator/llm_client.py` → `RATE_LIMIT_BUFFER = 10`

## After Generation

### Build for Production
```bash
cd website
npm run build
```

### Deploy to Vercel (or similar)
```bash
cd website
npm run deploy
```

### Test Mobile Performance
- Open on mobile device
- Verify <3 second load time
- Check smooth 60 FPS scrolling

## Phase 4: Summaries (Next)

After chapters are generated, implement:
- T038-T045: Chapter summaries (3-5 takeaways each)
- Uses Haiku model (faster/cheaper)
- Appended to chapter markdown

---

**Ready?** Set your API key and run:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
cd /c/Users/Dell/Desktop/book
PYTHONPATH=. python scripts/generate_chapters.py
```

**Time to generate**: ⏱️ 10-15 minutes
**Result**: 🎓 Complete AI-Native Textbook ready for learners!
