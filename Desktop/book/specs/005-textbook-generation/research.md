# Research: Textbook Content Generation

**Feature**: 005-textbook-generation
**Date**: 2025-12-10
**Status**: Complete

## Executive Summary

Research findings for AI-powered textbook content generation covering LLM selection, Docusaurus configuration, validation strategies, curriculum design, and batch generation workflows. All decisions prioritize free-tier compatibility, simplicity, and alignment with constitution principles.

---

## Research Task 1: LLM Selection for Content Generation

### Decision

**Selected**: Anthropic Claude API (Claude 3.5 Sonnet or Claude 3 Haiku) via free-tier credits

### Rationale

1. **Free-Tier Availability**: Anthropic provides API credits for new users; alternative is to use Claude Code's existing integration
2. **Content Quality**: Claude excels at educational content generation with clear structure and appropriate tone
3. **Token Efficiency**: Claude's context window and output quality reduce regeneration needs
4. **Rate Limits**: Manageable with batch processing and retry logic (free tier: ~50 requests/day typical)
5. **Alignment**: Claude's instruction-following is excellent for structured outputs (summaries, quizzes)

### Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| OpenAI GPT-4 | Excellent quality | More expensive, stricter rate limits | Rejected |
| OpenAI GPT-3.5 | Faster, cheaper | Lower quality for educational content | Backup option |
| Open-source (Llama 3) | Truly free, no limits | Requires local GPU, quality concerns | Rejected (complexity) |
| Gemini (Google) | Competitive quality | Less mature API, unclear free tier | Rejected |

### Implementation Notes

- Use Claude 3 Haiku for summaries and quiz questions (faster, cheaper)
- Use Claude 3.5 Sonnet for chapter content and learning boosters (higher quality)
- Implement exponential backoff for rate limit handling
- Cache generated content to avoid regeneration costs
- Monitor token usage per chapter (estimate: 2000-3000 tokens per chapter generation)

### Free-Tier Budget

- **Estimated total tokens**: ~60,000 tokens (8 chapters × 7,500 tokens avg per chapter with enhancements)
- **Free tier limit**: Varies by plan (typically $5-10 credit = ~100K-200K tokens)
- **Risk mitigation**: Start with 6 chapters, expand to 8 if budget allows

---

## Research Task 2: Docusaurus Configuration Best Practices

### Decision

**Configuration**: Docusaurus with MDX support, custom React components for quizzes and learning boosters

### Rationale

1. **MDX Support**: Enables embedding React components (quizzes, boosters) directly in markdown
2. **Simple Configuration**: Docusaurus requires minimal setup for docs-only sites
3. **Static Generation**: Fast loading, SEO-friendly, mobile-optimized by default
4. **Component Integration**: Custom components for interactive elements without JavaScript frameworks

### Configuration Details

```yaml
# docusaurus.config.js key settings
docs:
  routeBasePath: '/'           # Docs as homepage
  sidebarPath: './sidebars.js' # Auto-generated from chapter files
  remarkPlugins: []            # Minimal plugins for speed
  rehypePlugins: []

theme:
  customCss: './src/css/custom.css' # Minimal custom styles
```

### Content Structure

```text
website/docs/
├── intro.md                    # Landing page (chapter overview)
├── 01-physical-ai-intro.md
├── 02-humanoid-robotics.md
├── 03-sensors-actuators.md
├── 04-perception-systems.md
├── 05-motion-planning.md
├── 06-learning-control.md
└── 07-ethics-safety.md (optional)
└── 08-future-trends.md (optional)
```

### Component Strategy

**Quiz Component** (`src/components/ChapterQuiz.tsx`):
- Props: `questions` (array), `chapterId` (string)
- Features: Multiple choice, immediate feedback, score tracking
- No backend integration in MVP (client-side only)

**Learning Booster Component** (`src/components/LearningBooster.tsx`):
- Props: `type` (analogy/example/explanation), `content` (string)
- Styling: Callout box with icon, distinct background color
- Accessibility: Proper ARIA labels, semantic HTML

### Alternatives Considered

- **Pure Markdown**: Rejected (no interactive quizzes)
- **VuePress**: Rejected (Vue vs React ecosystem, less Docusaurus momentum)
- **MkDocs**: Rejected (Python-based, less modern component support)

---

## Research Task 3: Content Validation Strategy

### Decision

**Validation Stack**: Python markdown validation + custom content rules + quiz correctness checks

### Rationale

1. **Fast Validation**: Python libraries provide <1s validation per chapter
2. **Automated Checks**: Catch errors before manual review
3. **Clear Errors**: Structured error messages for debugging
4. **Pre-Publish Gate**: Prevents malformed content from reaching Docusaurus

### Validation Layers

#### Layer 1: Markdown Syntax Validation
- **Tool**: `markdown-it-py` or `mistune` (Python markdown parsers)
- **Checks**: Valid markdown syntax, no malformed headers, proper list formatting
- **Performance**: <100ms per chapter

#### Layer 2: Content Structure Validation
- **Custom Rules**:
  - Chapter has exactly 1 H1 heading (title)
  - Learning objectives section present
  - Word count between 800-1200 words
  - Exactly 3-5 summary takeaways
  - Exactly 5-7 quiz questions
  - Exactly 2-3 learning boosters
- **Implementation**: Python regex + AST parsing

#### Layer 3: Quiz Correctness Validation
- **Checks**:
  - Each question has exactly 4 answer options
  - Each question has exactly 1 correct answer
  - No duplicate questions
  - Questions are relevant to chapter (keyword matching)
- **Implementation**: Custom validator in `agents/content_generator/validator.py`

#### Layer 4: Docusaurus Build Test
- **Check**: Run `docusaurus build` on generated content
- **Purpose**: Catch MDX syntax errors, broken links, missing components
- **Performance**: ~10-30s for full build

### Validation Workflow

```python
# agents/content_generator/validator.py

class ContentValidator:
    def validate_chapter(self, chapter_md: str) -> ValidationResult:
        # Layer 1: Markdown syntax
        syntax_errors = validate_markdown_syntax(chapter_md)

        # Layer 2: Content structure
        structure_errors = validate_content_structure(chapter_md)

        # Layer 3: Word count
        word_count = count_words(chapter_md)
        if not (800 <= word_count <= 1200):
            structure_errors.append(f"Word count {word_count} outside range")

        return ValidationResult(
            valid=len(syntax_errors + structure_errors) == 0,
            errors=syntax_errors + structure_errors
        )

    def validate_quiz(self, quiz: Quiz) -> ValidationResult:
        # Layer 3: Quiz correctness
        # ... implementation
```

### Error Handling

- **Validation Failures**: Log error, mark chapter as FAILED, allow manual retry
- **Retry Logic**: Up to 3 automatic regeneration attempts with improved prompts
- **Manual Review Gate**: All generated content flagged for human review before publish

---

## Research Task 4: Curriculum Design for Physical AI & Robotics

### Decision

**Curriculum**: 6-8 chapters covering Physical AI fundamentals to advanced humanoid robotics applications

### Rationale

1. **Beginner-Friendly**: Assumes no prior robotics knowledge
2. **Industry Alignment**: Topics match current Physical AI research and applications
3. **Comprehensive Coverage**: Sensors to ethics in logical progression
4. **Constitution Compliance**: 6-8 chapters, each 5-7 minutes, education-focused

### Proposed Chapter Outline

#### Chapter 1: Introduction to Physical AI (P1 - MVP Core)
**Learning Objectives**:
- Define Physical AI and distinguish from traditional AI
- Understand the role of embodiment in intelligence
- Identify real-world applications of Physical AI

**Topics**: What is Physical AI, history, embodied intelligence, applications (industrial robots, drones, autonomous vehicles)

**Word Count Target**: 1000 words

---

#### Chapter 2: Humanoid Robotics Fundamentals (P1 - MVP Core)
**Learning Objectives**:
- Explain the motivation for humanoid form factors
- Describe key components of humanoid robots
- Understand design challenges and trade-offs

**Topics**: Why humanoid robots, anatomy (torso, limbs, head), degrees of freedom, balance and stability, examples (Atlas, Optimus, Digit)

**Word Count Target**: 1100 words

---

#### Chapter 3: Sensors and Perception (P1 - MVP Core)
**Learning Objectives**:
- Identify sensor types used in robotics
- Explain sensor fusion principles
- Understand perception pipelines

**Topics**: Vision (cameras, lidar), tactile sensors, IMUs, proprioception, sensor fusion, perception for navigation

**Word Count Target**: 1000 words

---

#### Chapter 4: Actuators and Motion (P1 - MVP Core)
**Learning Objectives**:
- Describe actuator technologies
- Explain motion control principles
- Understand gait generation for humanoid robots

**Topics**: Motors (servo, stepper), hydraulics, pneumatics, motion control (PID, MPC), bipedal locomotion, gait patterns

**Word Count Target**: 1050 words

---

#### Chapter 5: AI for Robot Control (P2 - Extended)
**Learning Objectives**:
- Explain reinforcement learning for robotics
- Understand imitation learning approaches
- Identify challenges in sim-to-real transfer

**Topics**: RL basics, policy learning, sim-to-real gap, imitation learning, end-to-end learning, teleoperation

**Word Count Target**: 1100 words

---

#### Chapter 6: Manipulation and Dexterity (P2 - Extended)
**Learning Objectives**:
- Describe grasp planning techniques
- Explain manipulation primitives
- Understand dexterous manipulation challenges

**Topics**: Grasping, manipulation planning, force control, dexterous hands, tool use, object manipulation

**Word Count Target**: 1000 words

---

#### Chapter 7: Safety and Ethics (P3 - Optional)
**Learning Objectives**:
- Identify safety considerations in humanoid robotics
- Understand ethical implications of embodied AI
- Explain regulatory landscape

**Topics**: Safety standards (ISO), human-robot interaction safety, ethical concerns, bias in robotics, regulation

**Word Count Target**: 900 words

---

#### Chapter 8: Future Trends and Applications (P3 - Optional)
**Learning Objectives**:
- Explore emerging applications of humanoid robots
- Understand current research frontiers
- Envision future developments

**Topics**: Healthcare robots, service robots, space exploration, research challenges (long-term autonomy, generalization), future vision

**Word Count Target**: 950 words

### Curriculum Justification

- **Progression**: Builds from fundamentals (Ch 1-2) to systems (Ch 3-4) to intelligence (Ch 5-6) to societal impact (Ch 7-8)
- **Practical Focus**: Real-world examples (Atlas, Optimus) and applications throughout
- **No Code**: Education-focused explanations without complex algorithms (constitution compliant)
- **Balanced Depth**: Each chapter covers breadth without overwhelming detail (5-7 min read target)

### MVP vs Extended

- **MVP (6 chapters)**: Ch 1-6 (covers fundamentals through AI control and manipulation)
- **Extended (8 chapters)**: Add Ch 7-8 (safety/ethics and future trends)
- **Decision Point**: Start with 6 chapters, add 7-8 if free-tier budget allows

---

## Research Task 5: Batch Generation Workflow

### Decision

**Workflow**: Sequential generation with parallel enhancement generation, exponential backoff retry, progress tracking in database

### Rationale

1. **Sequential Main Generation**: Prevents rate limit issues, easier debugging
2. **Parallel Enhancements**: Summaries/quizzes/boosters can generate in parallel (no dependencies)
3. **Retry Logic**: Handles transient API failures gracefully
4. **Progress Tracking**: Database tracks status for resumable generation

### Generation Workflow

```text
┌─────────────────────────────────────────────────┐
│ Step 1: Initialize Generation Job               │
│ - Create GenerationJob record (status=pending)  │
│ - Load curriculum (chapter topics)              │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Step 2: Sequential Chapter Generation           │
│ FOR each chapter in curriculum:                 │
│   - Generate chapter content (LLM call)         │
│   - Validate markdown syntax                    │
│   - Validate word count (800-1200)              │
│   - Save Chapter record (status=generated)      │
│   - Wait 5s (rate limit buffer)                 │
│ IF any failure: Log error, mark job FAILED      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Step 3: Parallel Enhancement Generation         │
│ FOR each generated chapter (in parallel):       │
│   ├─ Generate summary (3-5 takeaways)           │
│   ├─ Generate quiz (5-7 questions)              │
│   └─ Generate boosters (2-3 callouts)           │
│ Collect all results, validate completeness      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Step 4: Content Assembly & Validation           │
│ FOR each chapter:                                │
│   - Merge chapter + summary + quiz + boosters   │
│   - Validate final markdown structure           │
│   - Write to /website/docs/{chapter}.md         │
│   - Update Chapter record (status=published)    │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Step 5: Docusaurus Build Test                   │
│ - Run `docusaurus build`                        │
│ - IF build succeeds: Mark job COMPLETED         │
│ - IF build fails: Log errors, mark FAILED       │
└─────────────────────────────────────────────────┘
```

### Retry Logic

```python
# agents/content_generator/chapter_generator.py

def generate_chapter_with_retry(
    chapter_num: int,
    topic: str,
    max_retries: int = 3
) -> str:
    """Generate chapter with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            content = llm_generate_chapter(topic, word_count_target=1000)

            # Validate
            validation = validator.validate_chapter(content)
            if validation.valid:
                return content

            # Invalid - retry with improved prompt
            logger.warning(f"Chapter {chapter_num} validation failed: {validation.errors}")

        except RateLimitError as e:
            wait_time = 2 ** attempt * 5  # 5s, 10s, 20s
            logger.info(f"Rate limited, waiting {wait_time}s")
            time.sleep(wait_time)

        except Exception as e:
            logger.error(f"Generation failed: {e}")

    raise GenerationError(f"Failed to generate chapter {chapter_num} after {max_retries} attempts")
```

### Progress Tracking

**Database Schema** (GenerationJob table):
```python
class GenerationJob:
    id: UUID
    started_at: datetime
    completed_at: Optional[datetime]
    status: Enum["pending", "in_progress", "completed", "failed"]
    chapters_completed: int
    chapters_total: int
    errors: List[str]
    token_usage: int
```

**Status Checks**:
- `GET /api/content/generation-status` returns current job progress
- Frontend can poll for status updates (optional feature)
- Logs provide detailed progress for debugging

### Estimated Timeline

- **Chapter Generation**: 6 chapters × 2 min avg = 12 minutes
- **Enhancement Generation**: 6 chapters × 3 enhancements × 30s = 9 minutes (parallel)
- **Validation & Assembly**: 6 chapters × 30s = 3 minutes
- **Docusaurus Build**: 30 seconds
- **Buffer for Retries**: 30 minutes
- **Total Estimated Time**: ~55 minutes (well under 2-hour target)

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Fully Parallel | Fastest (all chapters at once) | High rate limit risk, harder to debug | Rejected |
| Fully Sequential | Simple, no rate limit issues | Slow (~90 min total) | Rejected (enhancements can parallelize) |
| Hybrid (chosen) | Balanced speed and reliability | Moderate complexity | **Selected** |
| Real-Time Generation | On-demand content | High latency, rate limit issues | Rejected (out of scope) |

---

## Technology Stack Summary

### Content Generation
- **LLM**: Anthropic Claude (3.5 Sonnet for chapters, 3 Haiku for enhancements)
- **Language**: Python 3.11+
- **Validation**: `markdown-it-py` + custom validators
- **Storage**: Markdown files + Neon PostgreSQL (metadata) + Qdrant (embeddings)

### Content Delivery
- **Framework**: Docusaurus (latest stable)
- **Components**: React (MDX) for quizzes and learning boosters
- **Styling**: Docusaurus theming + minimal custom CSS
- **Deployment**: Vercel (automatic deploys from main branch)

### Workflow Orchestration
- **Generation**: Python batch scripts in `/agents/content_generator/`
- **Retry Logic**: Exponential backoff with max 3 attempts
- **Progress Tracking**: PostgreSQL (GenerationJob table)
- **Validation**: Multi-layer (syntax → structure → quiz → build test)

---

## Risk Mitigation

### Risk 1: Free-Tier Token Limits Exceeded
**Mitigation**: Start with 6 chapters (not 8), monitor token usage, implement caching

### Risk 2: API Rate Limiting
**Mitigation**: Sequential generation with 5s buffers, exponential backoff retry

### Risk 3: Low Content Quality
**Mitigation**: Human review gate, regeneration with improved prompts, validation layers

### Risk 4: Docusaurus Build Failures
**Mitigation**: Pre-build markdown validation, test build in CI/CD pipeline

### Risk 5: Generation Takes >2 Hours
**Mitigation**: Hybrid parallelization, optimized prompts, early estimation tests

---

## Next Steps

1. ✅ Research complete - all technical decisions documented
2. ⏳ Create data-model.md based on entities defined here
3. ⏳ Generate contracts/content-generation-api.yaml (OpenAPI spec)
4. ⏳ Write quickstart.md for running content generation workflow
5. ⏳ Update plan.md with research findings
6. ⏳ Proceed to Phase 1 (data model and contracts)
