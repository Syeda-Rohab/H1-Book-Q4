---
id: 001
title: Create AI-Native Textbook Constitution
stage: constitution
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 004-vla-robotics
user: Dell
command: /sp.constitution
labels: ["constitution", "ai-native", "textbook", "physical-ai", "robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Project constitution : AI-Native Textbook for physical AI & humanoid robotics

1)Mission
Build a fully AI-Native , interactive , intelligent textbook that teaches the physical.the product must be fast ,simple , beautiful and feel like a REAL AI-powered education book

2)Core delivererables
1. A docusaurus based interactive textbook with 6-8 short , clean , modern chapters .
2. A fully functional RAG chatbot answering questions ONLY from the book.
3. User authentication (sign-up/login)using better-Auth
4. Personalized chapter content based on user background
5. One-click urdu translation for every chapter
6. Auto-generated summaries, quizzes , and learning boosters

3) Success Criteria

CLEAN UI , fast loading , mobile friendly
Book readable in < 50 minutes total
RAG answer accurate , cited and grounded
Personalization visibly improves text
Urdu translation high-quality and fast
Fully deployed
Front-end - vercel
Backend - railway
Vectors - qdrant
Database - neon

4)Non-goals

No extra animations beyond minimal useful motion
No overly long chapters (short + clear only)
No complex robotics code - only education content


5) architecture and principles
Keep frontend extremely simple , readable
Keep backend modular (fast API +services+routes)
All data must be stored clearly in neon + qdrant
Use clean folder structure
'/backend '
'/website'
'/Rag'
'/agents'
Use reusable agent skills for bonus scoring

6)use stories (prioritized)

1. As a learner : I want to read the textbook smoothly
2. As a learner : I want to ask the chatbot questions
3. As a learner : 3.  I want personalized content based on my background
4. As a learner : I want Urdu translation
5. As a learner : I want summaries + quizzes
6. As a learner: I want clean architecture and deployment

7) Constraints

Must work on free tiers (Qdrant+Neon)
Must support low-end devices (users reading on phones)
Must avoid complexity and heavy dependencies

8)Risks & mitigation
RAG LOW ACCURACY* use chunking+ miniLM embedding
Token usage High - implement in phases
User confusion keep UI minimal and clean
Backend errors (add health checks + logging)


9) Definition of Done

All chapters visible and reusable
Chatbot fully functional with grounded answers
Auth + personalization + translation working
Quizzes + summaries per chapter generated
Fully deployed URLs live and stable
75-second Demo recorded

## Response snapshot

Created comprehensive AI-Native Textbook Constitution v1.0.0 with 8 core principles:

1. AI-Native Design - AI embedded in every interaction
2. Speed & Simplicity - Fast, minimal, <50min reading time
3. Free-Tier Architecture - Qdrant, Neon, Vercel, Railway
4. Grounded RAG Responses - Cited, accurate, no hallucinations
5. Modular Backend Structure - FastAPI with models/services/routes
6. Mobile-First Responsive Design - Low-end devices, 3G support
7. Content Quality Over Quantity - 6-8 chapters, 5-7min each
8. Observability & Health Monitoring - Logging, health checks

Additional sections: Architecture & Technology Stack, User Experience Standards, Deployment & Operations, Governance.

All templates validated. Version 1.0.0 ratified 2025-12-10.

## Outcome

- ✅ Impact: Constitution establishes clear principles for AI-Native Textbook project
- 🧪 Tests: Template compatibility validated (plan, spec, tasks templates)
- 📁 Files: .specify/memory/constitution.md (231 lines, 8 principles)
- 🔁 Next prompts: /sp.specify or /sp.plan for feature work
- 🧠 Reflection: Non-negotiable constraints prevent architectural drift

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor first feature spec for principle validation
