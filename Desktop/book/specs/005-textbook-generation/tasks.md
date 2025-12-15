---

description: "Task list for textbook content generation feature"
---

# Tasks: Textbook Content Generation

**Input**: Design documents from `/specs/005-textbook-generation/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md

**Tests**: Tests are NOT required for this feature (content generation focused on AI outputs and manual validation)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/src/`, `website/`, `agents/content_generator/`
- Paths shown below use project root as base

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (backend/src/, website/, agents/content_generator/)
- [x] T002 Initialize Python project with pyproject.toml for backend and agents
- [x] T003 Initialize Node.js project with package.json for website
- [x] T004 [P] Create .env.example file with required environment variables (ANTHROPIC_API_KEY, DATABASE_URL)
- [x] T005 [P] Create .gitignore for Python, Node, and environment files
- [x] T006 [P] Install Python dependencies in backend/requirements.txt (fastapi, anthropic, asyncpg, alembic, markdown-it-py)
- [x] T007 [P] Install Node dependencies in website/package.json (docusaurus, react)
- [x] T008 [P] Install Python dependencies in agents/content_generator/requirements.txt (anthropic, markdown-it-py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create database migration script in backend/alembic/versions/001_initial_schema.py for all tables (generation_jobs, chapters, chapter_contents, summaries, quizzes, quiz_questions, learning_boosters)
- [x] T010 [P] Create database models in backend/src/models/generation_job.py
- [x] T011 [P] Create database models in backend/src/models/chapter.py
- [x] T012 [P] Create database models in backend/src/models/summary.py
- [x] T013 [P] Create database models in backend/src/models/quiz.py (Quiz and QuizQuestion models)
- [x] T014 [P] Create database models in backend/src/models/learning_booster.py
- [x] T015 Create curriculum definition in agents/content_generator/curriculum.py with 6-8 chapter topics from research.md
- [x] T016 Create base LLM client wrapper in agents/content_generator/llm_client.py (Anthropic API with retry logic)
- [x] T017 Create content validator framework in agents/content_generator/validator.py (markdown syntax, word count, structure validation)
- [x] T018 Configure Docusaurus in website/docusaurus.config.js (docs route, sidebar, theme)
- [x] T019 Create Docusaurus sidebar configuration in website/sidebars.js
- [x] T020 [P] Create health check endpoint in backend/src/routes/health_routes.py
- [x] T021 [P] Setup structured logging configuration in backend/src/utils/logging.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Read Interactive Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Generate 6-8 AI-powered textbook chapters on Physical AI & Humanoid Robotics that are readable, well-structured, and deployable via Docusaurus

**Independent Test**: Run batch generation, verify all chapters generated (800-1200 words each), load in Docusaurus dev server, navigate between chapters, confirm mobile-responsive and <3s load time on 3G

### Implementation for User Story 1

- [ ] T022 [P] [US1] Implement chapter generation prompts in agents/content_generator/prompts.py (system prompt, chapter template with learning objectives)
- [ ] T023 [US1] Implement ChapterGenerator class in agents/content_generator/chapter_generator.py (LLM API call, word count enforcement, retry logic)
- [ ] T024 [US1] Implement chapter validation in agents/content_generator/validator.py (800-1200 word check, markdown syntax, learning objectives present)
- [ ] T025 [US1] Implement ChapterService in backend/src/services/chapter_service.py (CRUD operations, status tracking)
- [ ] T026 [US1] Implement GenerationService orchestration in backend/src/services/generation_service.py (sequential chapter generation with 5s delays)
- [ ] T027 [US1] Implement POST /api/content/generate endpoint in backend/src/routes/content_routes.py (start batch generation job)
- [ ] T028 [US1] Implement GET /api/content/generation-status/{job_id} endpoint in backend/src/routes/content_routes.py
- [ ] T029 [US1] Implement GET /api/content/chapters endpoint in backend/src/routes/content_routes.py (list all chapters with metadata)
- [ ] T030 [US1] Implement GET /api/content/chapters/{chapter_number} endpoint in backend/src/routes/content_routes.py
- [ ] T031 [US1] Create markdown file writer in agents/content_generator/markdown_writer.py (write to website/docs/ with proper frontmatter)
- [ ] T032 [US1] Create Docusaurus intro page in website/docs/intro.md (textbook homepage with chapter overview)
- [ ] T033 [US1] Run generation for Chapter 1 (Introduction to Physical AI) and validate output
- [ ] T034 [US1] Run generation for Chapter 2 (Humanoid Robotics Fundamentals) and validate output
- [ ] T035 [US1] Run generation for Chapters 3-6 (Sensors, Actuators, AI Control, Manipulation) and validate outputs
- [ ] T036 [US1] Test Docusaurus build with npm run build in website/ directory
- [ ] T037 [US1] Verify mobile responsiveness and 3G load performance for all chapters

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (6 chapters readable in Docusaurus)

---

## Phase 4: User Story 2 - Access Chapter Summaries (Priority: P2)

**Goal**: Generate AI-powered summaries (3-5 key takeaways) for each chapter and display at chapter end

**Independent Test**: Open any chapter, scroll to end, verify summary section with 3-5 concise takeaways displayed, check uniqueness across chapters

### Implementation for User Story 2

- [ ] T038 [P] [US2] Implement summary generation prompts in agents/content_generator/prompts.py (3-5 takeaway format)
- [ ] T039 [US2] Implement SummaryGenerator class in agents/content_generator/summary_generator.py (LLM API call for summaries)
- [ ] T040 [US2] Implement summary validation in agents/content_generator/validator.py (3-5 takeaways check, length validation 50-150 chars each)
- [ ] T041 [US2] Add summary generation to GenerationService in backend/src/services/generation_service.py (parallel generation after chapters)
- [ ] T042 [US2] Update markdown_writer.py to embed summaries in chapter markdown (append to chapter content with heading)
- [ ] T043 [US2] Generate summaries for all 6 chapters in parallel
- [ ] T044 [US2] Validate summary quality (conciseness, relevance, uniqueness) for each chapter
- [ ] T045 [US2] Update Docusaurus styling in website/src/css/custom.css for summary sections (callout box styling)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (chapters + summaries)

---

## Phase 5: User Story 3 - Take AI-Generated Quizzes (Priority: P3)

**Goal**: Generate 5-7 multiple choice quiz questions per chapter with immediate feedback functionality

**Independent Test**: Open any chapter, click "Take Quiz", answer questions, receive immediate feedback on correctness, view final score

### Implementation for User Story 3

- [ ] T046 [P] [US3] Implement quiz generation prompts in agents/content_generator/prompts.py (5-7 questions, 4 options each, difficulty levels)
- [ ] T047 [US3] Implement QuizGenerator class in agents/content_generator/quiz_generator.py (LLM API call for quiz questions)
- [ ] T048 [US3] Implement quiz validation in agents/content_generator/validator.py (5-7 questions, exactly 1 correct answer, 4 options per question)
- [ ] T049 [US3] Add quiz generation to GenerationService in backend/src/services/generation_service.py (parallel generation after chapters)
- [ ] T050 [US3] Create ChapterQuiz React component in website/src/components/ChapterQuiz.tsx (multiple choice UI, answer feedback, score display)
- [ ] T051 [US3] Update markdown_writer.py to embed quiz data as MDX in chapter markdown
- [ ] T052 [US3] Generate quizzes for all 6 chapters in parallel
- [ ] T053 [US3] Validate quiz quality (question relevance, answer correctness, difficulty balance) for each chapter
- [ ] T054 [US3] Test quiz interaction (selecting answers, immediate feedback, score calculation) in Docusaurus dev server
- [ ] T055 [US3] Implement quiz answer randomization (shuffle options, keep correct index tracking)

**Checkpoint**: All user stories 1, 2, AND 3 should now be independently functional (chapters + summaries + quizzes)

---

## Phase 6: User Story 4 - View Learning Boosters (Priority: P4)

**Goal**: Generate 2-3 AI-powered learning boosters per chapter (analogies, examples, explanations) displayed as callout boxes

**Independent Test**: Open any chapter, identify 2-3 learning booster callouts, verify they provide relevant analogies/examples/explanations for surrounding content

### Implementation for User Story 4

- [ ] T056 [P] [US4] Implement booster generation prompts in agents/content_generator/prompts.py (analogy, example, explanation types)
- [ ] T057 [US4] Implement BoosterGenerator class in agents/content_generator/booster_generator.py (LLM API call for 2-3 boosters per chapter)
- [ ] T058 [US4] Implement booster validation in agents/content_generator/validator.py (2-3 boosters, 100-300 chars, type checking)
- [ ] T059 [US4] Add booster generation to GenerationService in backend/src/services/generation_service.py (parallel generation after chapters)
- [ ] T060 [US4] Create LearningBooster React component in website/src/components/LearningBooster.tsx (callout box with icon, type-specific styling)
- [ ] T061 [US4] Update markdown_writer.py to embed learning boosters as MDX components in chapter markdown (position boosters strategically)
- [ ] T062 [US4] Generate learning boosters for all 6 chapters in parallel (2-3 per chapter)
- [ ] T063 [US4] Validate booster quality (relevance to section, clarity, helpfulness) for each chapter
- [ ] T064 [US4] Test learning booster rendering and ARIA labels for accessibility in Docusaurus

**Checkpoint**: All user stories should now be independently functional (chapters + summaries + quizzes + boosters)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final deployment preparation

- [ ] T065 [P] Add error handling and logging throughout generation pipeline (chapter_generator.py, summary_generator.py, quiz_generator.py, booster_generator.py)
- [ ] T066 [P] Implement rate limiting and exponential backoff in llm_client.py (handle 429 errors gracefully)
- [ ] T067 [P] Add token usage tracking in GenerationService (store in generation_jobs table)
- [ ] T068 Run full batch generation for all 6 chapters with all enhancements (end-to-end test)
- [ ] T069 Validate constitution compliance: word counts 800-1200, reading times 5-7 min, 3-5 summaries, 5-7 quiz questions, 2-3 boosters
- [ ] T070 Test Docusaurus production build (npm run build) and verify no build errors
- [ ] T071 [P] Create quickstart validation script in scripts/validate_generation.py (check all chapters exist and are valid)
- [ ] T072 [P] Update README.md with content generation instructions and quickstart reference
- [ ] T073 Test mobile performance on low-end Android device (3G connection, 60 FPS scrolling)
- [ ] T074 Run accessibility audit with axe-core or similar tool (WCAG 2.1 AA compliance)
- [ ] T075 [P] Create deployment documentation in docs/deployment.md (Vercel setup, environment variables)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 chapters but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1 chapters but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with US1 chapters but independently testable

### Within Each User Story

- Prompts before generators
- Generators before validation
- Services before routes
- Backend routes before frontend components
- Generation before content validation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories (US1-US4) can start in parallel (if team capacity allows)
- Within US2, US3, US4: prompts and generator classes can be developed in parallel
- All polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1 (Chapter Generation)

```bash
# These tasks can run in parallel within US1:
T022: Implement chapter generation prompts
T031: Create markdown file writer
T032: Create Docusaurus intro page

# These must run sequentially:
T023: Implement ChapterGenerator (depends on T022 prompts)
T024: Implement validation (depends on T023 generator)
T025-T030: Services and routes (depend on models from Foundational)
T033-T035: Generate chapters (depends on T023-T030 pipeline)
T036: Build test (depends on T033-T035 content)
```

---

## Parallel Example: User Story 2 (Summaries)

```bash
# These tasks can run in parallel:
T038: Implement summary prompts
T040: Implement summary validation
T045: Update Docusaurus styling

# Sequential dependencies:
T039: SummaryGenerator (depends on T038)
T041: Update GenerationService (depends on T039)
T042: Update markdown_writer (depends on T041)
T043: Generate summaries (depends on T042)
T044: Validate summaries (depends on T043)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (chapter generation)
4. **STOP and VALIDATE**: Test User Story 1 independently (6 chapters readable in Docusaurus)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - 6 chapters!)
3. Add User Story 2 → Test independently → Deploy/Demo (chapters + summaries)
4. Add User Story 3 → Test independently → Deploy/Demo (chapters + summaries + quizzes)
5. Add User Story 4 → Test independently → Deploy/Demo (full feature set)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (chapters) - PRIORITY
   - Developer B: User Story 2 (summaries)
   - Developer C: User Story 3 (quizzes)
   - Developer D: User Story 4 (boosters)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests required (content generation relies on AI outputs and manual validation)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Phase 1 (Setup)**: 8 tasks
- **Phase 2 (Foundational)**: 13 tasks
- **Phase 3 (User Story 1 - P1)**: 16 tasks
- **Phase 4 (User Story 2 - P2)**: 8 tasks
- **Phase 5 (User Story 3 - P3)**: 10 tasks
- **Phase 6 (User Story 4 - P4)**: 9 tasks
- **Phase 7 (Polish)**: 11 tasks

**Total**: 75 tasks

**Parallel Opportunities**: 22 tasks marked [P] can run in parallel within their phases

**Critical Path**: Setup → Foundational → US1 → Validation (~25 tasks for MVP)

**MVP Scope**: Phases 1-3 only (37 tasks) delivers 6 readable textbook chapters

**Full Feature**: All phases (75 tasks) delivers chapters + summaries + quizzes + boosters
