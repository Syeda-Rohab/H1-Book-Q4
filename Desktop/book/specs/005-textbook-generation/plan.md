# Implementation Plan: Textbook Content Generation

**Branch**: `005-textbook-generation` | **Date**: 2025-12-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-textbook-generation/spec.md`

## Summary

Generate 6-8 AI-powered textbook chapters on Physical AI and Humanoid Robotics with integrated summaries, quizzes, and learning boosters. Each chapter must be 800-1200 words (5-7 minute read), stored as Docusaurus-compatible markdown, with AI-generated enhancements that provide learning retention and self-assessment capabilities. This is the foundational content delivery feature for the AI-Native Textbook platform.

## Technical Context

**Language/Version**: Python 3.11+ (content generation scripts), Node.js 18+ (Docusaurus)
**Primary Dependencies**: OpenAI/Anthropic API (content generation), Docusaurus (static site), Python markdown libraries (validation)
**Storage**: Markdown files in `/website/docs/` (Docusaurus content), Neon PostgreSQL (metadata tracking), Qdrant (chapter embeddings for RAG)
**Testing**: pytest (Python generation scripts), Jest (Docusaurus content validation), manual content review
**Target Platform**: Content generation runs offline/batch, output deployed to Vercel via Docusaurus
**Project Type**: Web application (Docusaurus frontend + Python generation backend)
**Performance Goals**: Generation completes within 2 hours for all chapters, markdown validation <1 second per chapter
**Constraints**: Free-tier API limits (rate limiting, token budgets), 800-1200 words per chapter (constitution: Content Quality Over Quantity), no complex code examples
**Scale/Scope**: 6-8 chapters total, ~50-60 generated artifacts (chapters + summaries + quizzes + boosters)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: AI-Native Design ✅
- **Compliance**: Content generation uses LLM for chapters, summaries, quizzes, and learning boosters
- **Validation**: All generated content is AI-powered by default; no manual content creation in MVP

### Principle II: Speed & Simplicity ✅
- **Compliance**: 6-8 chapters (not more), 800-1200 words each, simple markdown format
- **Validation**: Generation scripts are straightforward batch processes, no real-time complexity
- **Risk**: Must ensure generation API calls don't introduce unnecessary complexity

### Principle III: Free-Tier Architecture ✅
- **Compliance**: Uses free-tier LLM API (with rate limiting), Docusaurus (free), Vercel (free hosting)
- **Validation**: Token budgets must be monitored to stay within free limits
- **Risk**: Content generation may require careful prompt engineering to minimize token usage

### Principle IV: Grounded RAG Responses ⚠️ PARTIAL
- **Compliance**: This feature generates source content for RAG; RAG implementation is separate
- **Validation**: Generated chapters will be chunked and embedded for RAG pipeline (separate feature)
- **Note**: This feature must ensure content is factually accurate for downstream RAG grounding

### Principle V: Modular Backend Structure ✅
- **Compliance**: Generation scripts in `/agents/content_generator/`, clear separation of concerns
- **Validation**: Chapter generation, summary generation, quiz generation, booster generation as separate modules

### Principle VI: Mobile-First Responsive Design ✅
- **Compliance**: Docusaurus handles responsive design; generated markdown is mobile-friendly
- **Validation**: Content structure (headings, paragraphs, lists) optimized for mobile reading

### Principle VII: Content Quality Over Quantity ✅
- **Compliance**: Exactly 6-8 chapters, strict 800-1200 word limit per chapter
- **Validation**: Generation scripts enforce word count limits; content validation rejects oversized chapters

### Principle VIII: Observability & Health Monitoring ✅
- **Compliance**: Generation logs track progress, errors, token usage, validation failures
- **Validation**: Structured logging for all generation steps, health status tracked in database

**Gate Status**: PASS ✅ (Principle IV partial compliance acceptable - RAG implementation is separate feature)

## Project Structure

### Documentation (this feature)

```text
specs/005-textbook-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── content-generation-api.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── chapter.py           # Chapter metadata model
│   │   ├── summary.py           # Summary model
│   │   ├── quiz.py              # Quiz and question models
│   │   └── generation_job.py   # Job tracking model
│   ├── services/
│   │   ├── chapter_service.py   # Chapter CRUD operations
│   │   └── generation_service.py # Generation orchestration
│   └── routes/
│       └── content_routes.py    # Content generation API endpoints
└── tests/
    ├── unit/
    │   ├── test_chapter_service.py
    │   └── test_generation_service.py
    └── integration/
        └── test_content_generation_flow.py

website/
├── docs/                        # Generated Docusaurus chapters
│   ├── chapter-01-intro.md
│   ├── chapter-02-...md
│   └── ...
├── src/
│   └── components/
│       ├── ChapterQuiz.tsx      # Quiz component
│       └── LearningBooster.tsx  # Booster callout component
└── docusaurus.config.js

agents/
├── content_generator/
│   ├── __init__.py
│   ├── chapter_generator.py     # Chapter content generation
│   ├── summary_generator.py     # Summary generation
│   ├── quiz_generator.py        # Quiz question generation
│   ├── booster_generator.py     # Learning booster generation
│   ├── validator.py             # Content validation
│   └── curriculum.py            # Chapter topic definitions
└── tests/
    ├── test_chapter_generator.py
    ├── test_quiz_generator.py
    └── test_validator.py
```

**Structure Decision**: Web application structure selected (Option 2). Frontend is Docusaurus for static content delivery, backend provides content generation API and metadata tracking, agents directory contains AI generation scripts per constitution's modular architecture principle. This separates concerns clearly: generation logic in `/agents`, API/persistence in `/backend`, content delivery in `/website`.

## Complexity Tracking

> No constitution violations - no complexity justification needed.

---

## Phase 0: Research & Technology Decisions

*Status: ✅ Complete - See research.md*

### Research Tasks

1. **LLM Selection for Content Generation**
   - Decision needed: OpenAI GPT-4/GPT-3.5 vs Anthropic Claude vs Open-source models
   - Criteria: Free-tier availability, token limits, content quality, rate limits
   - Research: Compare token costs, API limits, and output quality for educational content

2. **Docusaurus Configuration Best Practices**
   - Decision needed: Optimal Docusaurus setup for 6-8 chapters with quizzes and boosters
   - Criteria: Simple configuration, MDX vs pure markdown, component integration
   - Research: Docusaurus best practices for educational content, custom components

3. **Content Validation Strategy**
   - Decision needed: How to validate markdown syntax, word count, quiz correctness
   - Criteria: Fast validation (<1s per chapter), automated checks, clear error messages
   - Research: Python markdown validation libraries, quiz validation patterns

4. **Curriculum Design for Physical AI & Robotics**
   - Decision needed: Which 6-8 topics to cover in textbook
   - Criteria: Industry standards, beginner-friendly, comprehensive coverage
   - Research: Existing Physical AI curricula, Humanoid Robotics fundamentals

5. **Batch Generation Workflow**
   - Decision needed: Sequential vs parallel generation, retry logic, progress tracking
   - Criteria: Completes within 2 hours, handles API failures gracefully
   - Research: Best practices for batch LLM generation with rate limiting

*Note: Research findings will be documented in research.md*

---

## Phase 1: Data Model & Contracts

*Status: ✅ Complete - See data-model.md, contracts/, quickstart.md*

### Data Model

**Entities** (to be detailed in data-model.md):
- Chapter (id, number, title, content, word_count, status, timestamps)
- Summary (id, chapter_id, takeaways[], model_used, status)
- Quiz (id, chapter_id, questions[], total_count, timestamp)
- QuizQuestion (id, quiz_id, question_text, options[], correct_index, difficulty, topic)
- LearningBooster (id, chapter_id, booster_type, content, section_ref, position)
- GenerationJob (id, chapter_number, status, started_at, completed_at, errors[])

### API Contracts

**Endpoints** (to be detailed in contracts/content-generation-api.yaml):
- `POST /api/content/generate` - Trigger batch generation for all chapters
- `POST /api/content/generate/{chapter_id}` - Regenerate specific chapter
- `GET /api/content/chapters` - List all chapters with metadata
- `GET /api/content/chapters/{id}` - Get chapter details
- `GET /api/content/generation-status` - Check generation job status

### Quickstart Guide

*Status: Pending (to be created in quickstart.md)*

## Phase 2: Task Breakdown

*Status: Pending - Use `/sp.tasks` command after Phase 1 completion*

---

## Next Steps

1. ✅ Complete Technical Context section
2. ✅ Execute Phase 0 research (research.md generation)
3. ✅ Create data-model.md based on spec entities
4. ✅ Generate API contracts (OpenAPI schema)
5. ✅ Write quickstart.md for content generation workflow
6. ✅ Re-evaluate Constitution Check post-design
7. ⏳ Run `/sp.tasks` to generate implementation tasks

---

## Phase 0 & Phase 1 Summary

### Research Findings (research.md)
- **LLM Selection**: Anthropic Claude (3.5 Sonnet for chapters, 3 Haiku for enhancements)
- **Docusaurus Config**: MDX with custom React components for quizzes and boosters
- **Validation Strategy**: 4-layer validation (syntax → structure → quiz → build test)
- **Curriculum**: 6-8 chapters on Physical AI & Humanoid Robotics (Ch 1-6 MVP, Ch 7-8 optional)
- **Generation Workflow**: Hybrid sequential/parallel with exponential backoff retry

### Data Model (data-model.md)
- **7 Core Entities**: GenerationJob, Chapter, ChapterContent, Summary, Quiz, QuizQuestion, LearningBooster
- **Storage**: Neon PostgreSQL (metadata) + Markdown files (/website/docs/) + Qdrant (embeddings - future)
- **Validation**: Constitution-compliant constraints (800-1200 words, 5-7 min read, 3-5 summaries, 5-7 questions, 2-3 boosters)

### API Contracts (contracts/content-generation-api.yaml)
- **5 Endpoints**: POST /generate, POST /generate/{chapter}, GET /generation-status, GET /chapters, GET /chapters/{id}
- **OpenAPI 3.0**: Full schema with examples, error responses, and health checks

### Quickstart (quickstart.md)
- **8-Step Guide**: Prerequisites → Dependencies → Migrations → Curriculum → Generation → Validation → Preview → Deploy
- **Estimated Time**: ~60 minutes (generation + validation)
- **Performance Benchmarks**: 55 min total time, 42K tokens, 100% validation pass rate

### Constitution Re-Check
All principles remain compliant post-design:
- ✅ AI-Native Design (LLM for all content)
- ✅ Speed & Simplicity (batch generation, simple markdown)
- ✅ Free-Tier Architecture (Anthropic free credits, within token budget)
- ✅ Modular Backend (clear separation: agents/backend/website)
- ✅ Content Quality Over Quantity (6-8 chapters, strict word limits)

**Ready for Phase 2**: Implementation task breakdown via `/sp.tasks`
