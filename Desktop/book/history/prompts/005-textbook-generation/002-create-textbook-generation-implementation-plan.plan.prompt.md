---
id: 002
title: Create Textbook Generation Implementation Plan
stage: plan
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5
feature: 005-textbook-generation
branch: 005-textbook-generation
user: Dell
command: /sp.plan
labels: ["plan", "implementation", "architecture", "textbook", "content-generation"]
links:
  spec: specs/005-textbook-generation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-textbook-generation/plan.md
  - specs/005-textbook-generation/research.md
  - specs/005-textbook-generation/data-model.md
  - specs/005-textbook-generation/contracts/content-generation-api.yaml
  - specs/005-textbook-generation/quickstart.md
tests:
  - null
---

## Prompt

$ARGUMENTS

## Response snapshot

Created comprehensive implementation plan for Textbook Content Generation (005-textbook-generation) including technical context, constitution compliance check, Phase 0 research, and Phase 1 design artifacts.

**Branch**: 005-textbook-generation
**Planning Complete**: Phases 0-1 ✅, Ready for Phase 2 (tasks)

### Phase 0: Research & Technology Decisions (research.md)

**LLM Selection**: Anthropic Claude API
- Claude 3.5 Sonnet for chapter content (higher quality)
- Claude 3 Haiku for summaries/quizzes (faster, cheaper)
- Free-tier compatible (~60K tokens for 6-8 chapters)
- Exponential backoff retry for rate limiting

**Docusaurus Configuration**:
- MDX support for React components (quizzes, learning boosters)
- Static site generation for fast loading
- Mobile-first responsive by default

**Content Validation Strategy**:
- 4-layer validation: Syntax → Structure → Quiz → Build test
- Python markdown validation (<1s per chapter)
- Automated checks before manual review

**Curriculum Design**:
- 6 core chapters (MVP): Physical AI intro, Humanoid robotics, Sensors, Actuators, AI control, Manipulation
- 2 optional chapters: Safety/ethics, Future trends
- Beginner-friendly progression, no complex code

**Batch Generation Workflow**:
- Hybrid: Sequential chapter generation + parallel enhancement generation
- Estimated time: 55 minutes (under 2-hour target)
- Database progress tracking for resumable generation

### Phase 1: Data Model & Contracts

**Data Model (data-model.md)**:
- 7 entities: GenerationJob, Chapter, ChapterContent, Summary, Quiz, QuizQuestion, LearningBooster
- Storage: Neon PostgreSQL (metadata) + Markdown files (content) + Qdrant (embeddings - future)
- Constitution-compliant validation: 800-1200 words, 5-7 min read, 3-5 summaries, 5-7 quiz questions, 2-3 boosters

**API Contracts (content-generation-api.yaml)**:
- OpenAPI 3.0 specification with 5 endpoints
- POST /api/content/generate (batch generation)
- POST /api/content/generate/{chapter_number} (single chapter regeneration)
- GET /api/content/generation-status/{job_id} (progress tracking)
- GET /api/content/chapters (list all)
- GET /api/content/chapters/{chapter_number} (full details)

**Quickstart Guide (quickstart.md)**:
- 8-step guide: Prerequisites → Dependencies → Migrations → Curriculum → Generation → Validation → Preview → Deploy
- Estimated completion time: 60 minutes
- Performance benchmarks: 55 min generation, 42K tokens, 100% validation pass rate

### Technical Context

- **Language**: Python 3.11+ (generation), Node.js 18+ (Docusaurus)
- **Dependencies**: FastAPI, Anthropic API, Docusaurus, Neon PostgreSQL, Qdrant
- **Storage**: Markdown files + PostgreSQL metadata + Vector embeddings
- **Testing**: pytest, Jest, manual content review
- **Performance**: 2-hour generation target, <2s page load on 3G
- **Scale**: 6-8 chapters, ~50-60 artifacts total

### Constitution Compliance

All 8 principles validated:
- ✅ AI-Native Design (LLM for all content generation)
- ✅ Speed & Simplicity (batch scripts, simple markdown)
- ✅ Free-Tier Architecture (token budget within limits)
- ✅ Grounded RAG (foundation content for RAG pipeline)
- ✅ Modular Backend (agents/backend/website separation)
- ✅ Mobile-First (Docusaurus responsive by default)
- ✅ Content Quality Over Quantity (6-8 chapters, strict limits)
- ✅ Observability (structured logging, job tracking)

**Project Structure**: Web application (backend API + Docusaurus frontend + agent scripts)

### Files Created

1. **plan.md** (247 lines): Full implementation plan with technical context, constitution check, project structure
2. **research.md** (580 lines): Detailed research findings for all technology decisions
3. **data-model.md** (520 lines): Complete entity definitions, relationships, validation rules, access patterns
4. **contracts/content-generation-api.yaml** (850 lines): OpenAPI 3.0 spec with all endpoints, schemas, examples
5. **quickstart.md** (420 lines): Step-by-step developer guide with code examples and troubleshooting

**Total**: ~2,600 lines of planning documentation

## Outcome

- ✅ Impact: Complete architectural plan for textbook content generation. All technical decisions documented and justified. Ready for implementation task breakdown.
- 🧪 Tests: Constitution compliance verified post-design. All principles remain satisfied. No complexity violations.
- 📁 Files: 5 planning artifacts created (plan, research, data model, API contracts, quickstart). Branch 005-textbook-generation ready for /sp.tasks.
- 🔁 Next prompts: `/sp.tasks` to generate implementation task breakdown by user story
- 🧠 Reflection: Planning phase identified optimal architecture (Anthropic Claude + Docusaurus + modular Python) that balances free-tier constraints with quality requirements. Hybrid generation workflow (sequential chapters + parallel enhancements) optimizes for both speed (<2 hours) and reliability (rate limit management). Data model enforces constitution principles at database level (word count, reading time, enhancement counts).

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning workflow completed without blockers. All research questions answered with justified decisions.
- Graders run and results (PASS/FAIL): Constitution check - PASS (all 8 principles compliant). Technical feasibility - PASS (free-tier viable, performance targets achievable).
- Prompt variant (if applicable): N/A (standard planning workflow)
- Next experiment (smallest change to try): Monitor `/sp.tasks` generation to validate if planning artifacts provide sufficient detail for autonomous task creation. Check if curriculum design in research.md is detailed enough for implementation without additional clarification.
