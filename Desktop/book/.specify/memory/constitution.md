<!--
SYNC IMPACT REPORT
===================
Version Change: 0.0.0 (new) → 1.0.0 (initial ratification)
Modified Principles: N/A (initial creation)
Added Sections:
  - All core principles (8 principles)
  - Architecture & Technology Stack
  - User Experience Standards
  - Deployment & Operations
  - Governance
Removed Sections: None
Templates Status:
  ✅ plan-template.md - Reviewed, aligns with constitution principles
  ✅ spec-template.md - Reviewed, aligns with user story prioritization
  ✅ tasks-template.md - Reviewed, aligns with testing and implementation standards
  ✅ Command files - Generic, no AI-specific references requiring updates
Follow-up TODOs: None
===================
-->

# AI-Native Textbook for Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. AI-Native Design
Every feature MUST be AI-powered and intelligent by default. The product is not a traditional textbook with AI features added—it IS an AI-native learning platform. This means:
- Content personalization driven by user background
- RAG chatbot as a first-class learning companion
- Auto-generated summaries, quizzes, and learning boosters
- One-click translation capabilities
- AI is the foundation, not an add-on

**Rationale**: The mission is to build a product that "feels like a REAL AI-powered education book," which requires AI to be embedded in every interaction, not bolted on afterward.

### II. Speed & Simplicity
Every component MUST be fast, simple, and minimal. This principle is NON-NEGOTIABLE:
- Clean UI with no unnecessary animations beyond minimal useful motion
- Fast loading on low-end devices
- Entire book readable in under 50 minutes
- No complex dependencies or heavy libraries
- No over-engineering or premature optimization

**Rationale**: Target users include learners on low-end devices. Speed and simplicity directly impact accessibility and learning effectiveness. Complexity is the enemy of both performance and maintainability.

### III. Free-Tier Architecture
All infrastructure MUST work on free tiers. This principle applies to:
- Qdrant (vector database) - free tier
- Neon (PostgreSQL) - free tier
- Vercel (frontend hosting) - free tier
- Railway (backend hosting) - free tier

Resource usage must be optimized to stay within free tier limits. No paid dependencies without explicit justification and user approval.

**Rationale**: Project accessibility and cost constraints require free-tier compatibility. This constraint forces good architectural decisions and efficient resource usage.

### IV. Grounded RAG Responses
RAG chatbot MUST answer questions ONLY from the book content. Every response must be:
- Accurate and grounded in source material
- Cited with chapter/section references
- Explicitly stating "I don't know" when questions fall outside book scope
- Never hallucinating or inventing information

Use chunking + MiniLM embeddings to maintain accuracy while managing token costs.

**Rationale**: Trust is critical for educational content. Hallucinated or ungrounded answers destroy learning outcomes and user confidence.

### V. Modular Backend Structure
Backend MUST follow a clean, modular FastAPI structure:
- Separate services for distinct concerns
- Clear routing layer
- Models isolated from business logic
- All data stored clearly in Neon (relational) + Qdrant (vectors)

Folder structure:
```
/backend
  /src
    /models      # Database models
    /services    # Business logic
    /routes      # API endpoints
  /tests
/website         # Docusaurus frontend
/rag             # RAG pipeline
/agents          # AI agent skills
```

**Rationale**: Modularity enables parallel development, testing, and maintenance. Clear separation of concerns prevents coupling and simplifies debugging.

### VI. Mobile-First Responsive Design
UI MUST be mobile-friendly and fully responsive. Requirements:
- Clean, readable typography on small screens
- Touch-friendly interaction targets
- Fast loading on 3G connections
- Progressive enhancement (works without JavaScript for core content)
- Tested on low-end Android devices

**Rationale**: Many learners access educational content on mobile devices. Mobile-first design ensures accessibility for the widest audience.

### VII. Content Quality Over Quantity
All chapters MUST be short, clear, and modern:
- 6-8 chapters maximum
- Each chapter readable in 5-7 minutes
- No overly long explanations
- No complex robotics code—education-focused only
- Clear learning objectives per chapter

**Rationale**: Attention spans are limited. Short, focused content improves completion rates and learning retention. Quality beats quantity.

### VIII. Observability & Health Monitoring
Backend services MUST include:
- Structured logging for all operations
- Health check endpoints
- Error tracking and reporting
- Performance monitoring within free-tier limits

Logging must be production-ready from day one, not added later.

**Rationale**: Early observability prevents debugging nightmares in production. Health checks enable reliable deployments and quick incident response.

## Architecture & Technology Stack

### Frontend
- **Framework**: Docusaurus (static site generation + React)
- **Styling**: Minimal CSS, Docusaurus theming
- **Deployment**: Vercel
- **Requirements**: Fast builds, SEO-friendly, markdown-based content

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Neon (PostgreSQL) for relational data
- **Vector Store**: Qdrant for embeddings
- **Auth**: Better-Auth for sign-up/login
- **Deployment**: Railway
- **Requirements**: Async operations, health checks, structured logging

### RAG Pipeline
- **Embeddings**: MiniLM (lightweight, fast)
- **Chunking Strategy**: Semantic chunking with overlap
- **Retrieval**: Top-K with relevance threshold
- **Response Generation**: Grounded, cited responses only

### AI Agents
- Reusable agent skills for:
  - Content personalization
  - Translation (Urdu)
  - Summary generation
  - Quiz generation
  - Learning booster creation

### Constraints
- Python 3.11+ for backend
- Node.js 18+ for frontend
- Docker for local development (optional)
- All dependencies must work on free tiers

## User Experience Standards

### Performance Targets
- **Page Load**: < 2 seconds on 3G
- **RAG Response**: < 5 seconds end-to-end
- **Translation**: < 3 seconds per chapter
- **Mobile Performance**: 60 FPS scrolling, no jank

### Accessibility
- WCAG 2.1 AA compliance for core reading experience
- Keyboard navigation for all interactive elements
- Screen reader friendly
- High contrast mode support

### Personalization
- Background-based content adaptation
- User preferences persisted across sessions
- Non-intrusive, optional features

### Translation
- One-click Urdu translation per chapter
- High-quality translation (human-reviewed samples)
- Fast rendering without page reload

## Deployment & Operations

### Deployment Strategy
- **Frontend (Vercel)**: Automatic deploys from main branch
- **Backend (Railway)**: Manual deploys with health check validation
- **Database Migrations**: Alembic migrations, tested in staging first
- **Vector Updates**: Batch uploads, versioned embeddings

### Rollback Plan
- Frontend: Revert via Vercel dashboard (instant)
- Backend: Previous Railway deployment (< 2 minutes)
- Database: Migration rollback scripts required for every migration

### Monitoring
- Uptime checks for both frontend and backend
- Error rate tracking (target: < 1% error rate)
- Response time monitoring (target: p95 < 5s for API, < 2s for pages)
- Free-tier resource usage tracking (stay below 80% of limits)

## Governance

### Amendment Process
1. Proposed changes must document:
   - Reason for amendment
   - Impact on existing principles
   - Migration requirements (if any)
2. Amendments require explicit user approval
3. Version bump rules:
   - MAJOR: Backward incompatible principle changes
   - MINOR: New principle or significant expansion
   - PATCH: Clarifications, typos, non-semantic fixes
4. All amendments must update dependent templates and documentation

### Compliance Review
- All PRs must verify compliance with principles
- Architecture decisions checked against Section II (Speed & Simplicity) and Section V (Modular Backend)
- RAG responses audited against Section IV (Grounded RAG)
- UI changes validated against Section VI (Mobile-First) and Section II (Speed & Simplicity)

### Complexity Justification
Any violation of these principles requires explicit justification in plan.md:
- Why the violation is necessary
- Simpler alternatives considered and rejected
- Plan to remove the violation in future iterations

### Continuous Improvement
- Constitution reviewed after each major milestone
- Feedback from users incorporated into principle refinements
- Principle effectiveness measured against success criteria

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10
