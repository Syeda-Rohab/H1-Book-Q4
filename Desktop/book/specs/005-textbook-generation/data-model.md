# Data Model: Textbook Content Generation

**Feature**: 005-textbook-generation
**Date**: 2025-12-10
**Status**: Complete

## Overview

This document defines the data model for textbook content generation, including entities for chapters, summaries, quizzes, learning boosters, and generation job tracking. All entities are stored in Neon PostgreSQL for metadata and relationships, with chapter content stored as markdown files.

---

## Entity Relationship Diagram

```text
┌──────────────────┐
│ GenerationJob    │
│ ──────────────── │
│ id (PK)          │
│ started_at       │
│ completed_at     │
│ status           │
│ chapters_total   │
│ token_usage      │
└────────┬─────────┘
         │
         │ 1:N
         │
         ▼
┌──────────────────┐         ┌──────────────────┐
│ Chapter          │◄───────►│ ChapterContent   │
│ ──────────────── │  1:1    │ ──────────────── │
│ id (PK)          │         │ chapter_id (FK)  │
│ job_id (FK)      │         │ markdown_path    │
│ chapter_number   │         │ content_hash     │
│ title            │         │ docusaurus_url   │
│ word_count       │         └──────────────────┘
│ status           │
│ created_at       │
└────────┬─────────┘
         │
         │ 1:1
         │
         ▼
┌──────────────────┐
│ Summary          │
│ ──────────────── │
│ id (PK)          │
│ chapter_id (FK)  │
│ takeaways (JSON) │
│ model_used       │
│ generated_at     │
└──────────────────┘
         │
         │ 1:1
         │
         ▼
┌──────────────────┐         ┌──────────────────┐
│ Quiz             │         │ QuizQuestion     │
│ ──────────────── │  1:N    │ ──────────────── │
│ id (PK)          │◄────────│ id (PK)          │
│ chapter_id (FK)  │         │ quiz_id (FK)     │
│ total_questions  │         │ question_text    │
│ generated_at     │         │ options (JSON)   │
└──────────────────┘         │ correct_index    │
                              │ difficulty       │
                              │ topic            │
                              └──────────────────┘
         │
         │ 1:N
         │
         ▼
┌──────────────────┐
│ LearningBooster  │
│ ──────────────── │
│ id (PK)          │
│ chapter_id (FK)  │
│ booster_type     │
│ content          │
│ section_ref      │
│ position         │
│ generated_at     │
└──────────────────┘
```

---

## Entity Definitions

### 1. GenerationJob

Tracks the overall content generation process for a batch of chapters.

**Table**: `generation_jobs`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique job identifier |
| `started_at` | TIMESTAMP | NOT NULL | Job start timestamp |
| `completed_at` | TIMESTAMP | NULL | Job completion timestamp (null if in progress) |
| `status` | ENUM | NOT NULL | Job status: `pending`, `in_progress`, `completed`, `failed` |
| `chapters_completed` | INTEGER | DEFAULT 0 | Number of chapters successfully generated |
| `chapters_total` | INTEGER | NOT NULL | Total chapters to generate (6-8) |
| `errors` | JSONB | DEFAULT [] | Array of error messages encountered |
| `token_usage` | INTEGER | DEFAULT 0 | Total tokens consumed by LLM API |
| `model_used` | VARCHAR(100) | NOT NULL | LLM model identifier (e.g., "claude-3-5-sonnet-20241022") |

**Indexes**:
- `idx_generation_jobs_status` on `status`
- `idx_generation_jobs_started_at` on `started_at DESC`

**Validation Rules**:
- `status` must be one of: `pending`, `in_progress`, `completed`, `failed`
- `chapters_completed` must be <= `chapters_total`
- `token_usage` must be >= 0

**State Transitions**:
```
pending → in_progress → completed
                     ↘ failed
```

---

### 2. Chapter

Represents a single textbook chapter with metadata.

**Table**: `chapters`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique chapter identifier |
| `job_id` | UUID | FOREIGN KEY | References `generation_jobs(id)` |
| `chapter_number` | INTEGER | NOT NULL, UNIQUE | Chapter sequence number (1-8) |
| `title` | VARCHAR(255) | NOT NULL | Chapter title |
| `slug` | VARCHAR(255) | NOT NULL, UNIQUE | URL-friendly slug (e.g., "physical-ai-intro") |
| `word_count` | INTEGER | NOT NULL | Total word count (target: 800-1200) |
| `reading_time_minutes` | INTEGER | NOT NULL | Estimated reading time (target: 5-7) |
| `status` | ENUM | NOT NULL | Chapter status: `pending`, `generated`, `validated`, `published`, `failed` |
| `validation_errors` | JSONB | DEFAULT [] | Array of validation errors (if any) |
| `created_at` | TIMESTAMP | NOT NULL | Chapter creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**:
- `idx_chapters_job_id` on `job_id`
- `idx_chapters_number` on `chapter_number`
- `idx_chapters_status` on `status`

**Validation Rules**:
- `chapter_number` must be between 1 and 8
- `word_count` must be between 800 and 1200 (constitution compliance)
- `reading_time_minutes` must be between 5 and 7 (constitution compliance)
- `status` must be one of: `pending`, `generated`, `validated`, `published`, `failed`

**State Transitions**:
```
pending → generated → validated → published
                   ↘ failed
```

---

### 3. ChapterContent

Stores file system paths and content hashes for chapter markdown files.

**Table**: `chapter_contents`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique content identifier |
| `chapter_id` | UUID | FOREIGN KEY, UNIQUE | References `chapters(id)` (1:1 relationship) |
| `markdown_path` | VARCHAR(500) | NOT NULL | Relative path to markdown file (e.g., "docs/01-physical-ai-intro.md") |
| `content_hash` | VARCHAR(64) | NOT NULL | SHA-256 hash of markdown content (for change detection) |
| `docusaurus_url` | VARCHAR(500) | NOT NULL | Public URL after deployment (e.g., "/physical-ai-intro") |
| `stored_at` | TIMESTAMP | NOT NULL | Timestamp when file was written |

**Indexes**:
- `idx_chapter_contents_chapter_id` on `chapter_id`
- `idx_chapter_contents_hash` on `content_hash`

**Validation Rules**:
- `markdown_path` must match pattern: `docs/\d{2}-[a-z-]+\.md`
- `content_hash` must be 64-character hex string (SHA-256)

---

### 4. Summary

Stores AI-generated chapter summaries.

**Table**: `summaries`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique summary identifier |
| `chapter_id` | UUID | FOREIGN KEY, UNIQUE | References `chapters(id)` (1:1 relationship) |
| `takeaways` | JSONB | NOT NULL | Array of 3-5 summary points (strings) |
| `model_used` | VARCHAR(100) | NOT NULL | LLM model used for generation (e.g., "claude-3-haiku-20240307") |
| `validation_status` | ENUM | NOT NULL | Validation status: `valid`, `invalid`, `pending_review` |
| `generated_at` | TIMESTAMP | NOT NULL | Generation timestamp |

**Indexes**:
- `idx_summaries_chapter_id` on `chapter_id`
- `idx_summaries_validation_status` on `validation_status`

**Validation Rules**:
- `takeaways` array must contain 3-5 elements
- Each takeaway must be 1-2 sentences (50-150 chars)
- `validation_status` must be one of: `valid`, `invalid`, `pending_review`

**JSON Schema for `takeaways`**:
```json
{
  "type": "array",
  "minItems": 3,
  "maxItems": 5,
  "items": {
    "type": "string",
    "minLength": 50,
    "maxLength": 150
  }
}
```

---

### 5. Quiz

Represents a collection of quiz questions for a chapter.

**Table**: `quizzes`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique quiz identifier |
| `chapter_id` | UUID | FOREIGN KEY, UNIQUE | References `chapters(id)` (1:1 relationship) |
| `total_questions` | INTEGER | NOT NULL | Total number of questions (target: 5-7) |
| `model_used` | VARCHAR(100) | NOT NULL | LLM model used for generation |
| `validation_status` | ENUM | NOT NULL | Validation status: `valid`, `invalid`, `pending_review` |
| `generated_at` | TIMESTAMP | NOT NULL | Generation timestamp |

**Indexes**:
- `idx_quizzes_chapter_id` on `chapter_id`
- `idx_quizzes_validation_status` on `validation_status`

**Validation Rules**:
- `total_questions` must be between 5 and 7
- `validation_status` must be one of: `valid`, `invalid`, `pending_review`

---

### 6. QuizQuestion

Individual multiple-choice question within a quiz.

**Table**: `quiz_questions`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique question identifier |
| `quiz_id` | UUID | FOREIGN KEY | References `quizzes(id)` |
| `question_number` | INTEGER | NOT NULL | Question sequence within quiz (1-7) |
| `question_text` | TEXT | NOT NULL | Question text (50-200 chars) |
| `options` | JSONB | NOT NULL | Array of 4 answer options (strings) |
| `correct_index` | INTEGER | NOT NULL | Index of correct answer (0-3) |
| `difficulty` | ENUM | NOT NULL | Difficulty level: `easy`, `medium`, `hard` |
| `topic` | VARCHAR(255) | NOT NULL | Topic/concept being tested |
| `created_at` | TIMESTAMP | NOT NULL | Creation timestamp |

**Indexes**:
- `idx_quiz_questions_quiz_id` on `quiz_id`
- `idx_quiz_questions_difficulty` on `difficulty`

**Validation Rules**:
- `options` array must contain exactly 4 elements
- `correct_index` must be between 0 and 3
- `difficulty` must be one of: `easy`, `medium`, `hard`
- `question_text` must be between 50 and 200 characters
- Each option must be between 10 and 100 characters

**JSON Schema for `options`**:
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 10,
    "maxLength": 100
  },
  "minItems": 4,
  "maxItems": 4
}
```

---

### 7. LearningBooster

AI-generated supplementary content (analogies, examples, explanations).

**Table**: `learning_boosters`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique booster identifier |
| `chapter_id` | UUID | FOREIGN KEY | References `chapters(id)` |
| `booster_type` | ENUM | NOT NULL | Type: `analogy`, `example`, `explanation` |
| `content` | TEXT | NOT NULL | Booster content (100-300 chars) |
| `section_ref` | VARCHAR(255) | NOT NULL | Reference to related section heading |
| `position` | INTEGER | NOT NULL | Position within chapter (1-3) |
| `model_used` | VARCHAR(100) | NOT NULL | LLM model used for generation |
| `validation_status` | ENUM | NOT NULL | Validation status: `valid`, `invalid`, `pending_review` |
| `generated_at` | TIMESTAMP | NOT NULL | Generation timestamp |

**Indexes**:
- `idx_learning_boosters_chapter_id` on `chapter_id`
- `idx_learning_boosters_type` on `booster_type`
- `idx_learning_boosters_validation_status` on `validation_status`

**Validation Rules**:
- `booster_type` must be one of: `analogy`, `example`, `explanation`
- `content` must be between 100 and 300 characters
- `position` must be between 1 and 3
- Each chapter must have exactly 2-3 boosters
- `validation_status` must be one of: `valid`, `invalid`, `pending_review`

---

## Relationships Summary

| Parent | Child | Type | Constraint |
|--------|-------|------|------------|
| GenerationJob | Chapter | 1:N | CASCADE delete |
| Chapter | ChapterContent | 1:1 | CASCADE delete |
| Chapter | Summary | 1:1 | CASCADE delete |
| Chapter | Quiz | 1:1 | CASCADE delete |
| Chapter | LearningBooster | 1:N | CASCADE delete (2-3 boosters per chapter) |
| Quiz | QuizQuestion | 1:N | CASCADE delete (5-7 questions per quiz) |

---

## Database Migrations

### Migration 001: Initial Schema

```sql
-- Create ENUMs
CREATE TYPE job_status AS ENUM ('pending', 'in_progress', 'completed', 'failed');
CREATE TYPE chapter_status AS ENUM ('pending', 'generated', 'validated', 'published', 'failed');
CREATE TYPE validation_status AS ENUM ('valid', 'invalid', 'pending_review');
CREATE TYPE booster_type AS ENUM ('analogy', 'example', 'explanation');
CREATE TYPE question_difficulty AS ENUM ('easy', 'medium', 'hard');

-- Create tables (see entity definitions above for full DDL)
CREATE TABLE generation_jobs (...);
CREATE TABLE chapters (...);
CREATE TABLE chapter_contents (...);
CREATE TABLE summaries (...);
CREATE TABLE quizzes (...);
CREATE TABLE quiz_questions (...);
CREATE TABLE learning_boosters (...);

-- Create indexes (see entity definitions above)
CREATE INDEX idx_generation_jobs_status ON generation_jobs(status);
-- ... (all other indexes)
```

---

## Data Access Patterns

### Pattern 1: Start New Generation Job
```sql
INSERT INTO generation_jobs (id, status, chapters_total, model_used, started_at)
VALUES (gen_random_uuid(), 'pending', 6, 'claude-3-5-sonnet-20241022', NOW())
RETURNING id;
```

### Pattern 2: Retrieve Generation Job Status
```sql
SELECT
    gj.id,
    gj.status,
    gj.chapters_completed,
    gj.chapters_total,
    gj.token_usage,
    gj.started_at,
    gj.completed_at,
    COALESCE(gj.errors, '[]'::jsonb) AS errors
FROM generation_jobs gj
WHERE gj.id = :job_id;
```

### Pattern 3: List All Chapters with Enhancements
```sql
SELECT
    c.id,
    c.chapter_number,
    c.title,
    c.word_count,
    c.status,
    cc.docusaurus_url,
    s.takeaways,
    q.total_questions,
    COUNT(lb.id) AS booster_count
FROM chapters c
LEFT JOIN chapter_contents cc ON c.id = cc.chapter_id
LEFT JOIN summaries s ON c.id = s.chapter_id
LEFT JOIN quizzes q ON c.id = q.chapter_id
LEFT JOIN learning_boosters lb ON c.id = lb.chapter_id
GROUP BY c.id, cc.docusaurus_url, s.takeaways, q.total_questions
ORDER BY c.chapter_number;
```

### Pattern 4: Get Full Chapter Data for Rendering
```sql
-- Chapter + Summary + Quiz + Questions + Boosters
SELECT
    c.*,
    s.takeaways AS summary,
    q.id AS quiz_id,
    (
        SELECT json_agg(json_build_object(
            'id', qq.id,
            'question', qq.question_text,
            'options', qq.options,
            'correct', qq.correct_index,
            'difficulty', qq.difficulty
        ) ORDER BY qq.question_number)
        FROM quiz_questions qq
        WHERE qq.quiz_id = q.id
    ) AS quiz_questions,
    (
        SELECT json_agg(json_build_object(
            'type', lb.booster_type,
            'content', lb.content,
            'section', lb.section_ref,
            'position', lb.position
        ) ORDER BY lb.position)
        FROM learning_boosters lb
        WHERE lb.chapter_id = c.id
    ) AS learning_boosters
FROM chapters c
LEFT JOIN summaries s ON c.id = s.chapter_id
LEFT JOIN quizzes q ON c.id = q.chapter_id
WHERE c.chapter_number = :chapter_number;
```

---

## Validation Constraints (Application Layer)

### Chapter Validation
```python
def validate_chapter(chapter: Chapter) -> ValidationResult:
    errors = []

    # Word count constraint (constitution)
    if not (800 <= chapter.word_count <= 1200):
        errors.append(f"Word count {chapter.word_count} outside range [800, 1200]")

    # Reading time constraint (constitution)
    if not (5 <= chapter.reading_time_minutes <= 7):
        errors.append(f"Reading time {chapter.reading_time_minutes} outside range [5, 7]")

    # Title length
    if len(chapter.title) > 255:
        errors.append("Title exceeds 255 characters")

    return ValidationResult(valid=len(errors) == 0, errors=errors)
```

### Summary Validation
```python
def validate_summary(summary: Summary) -> ValidationResult:
    errors = []

    # Takeaway count (constitution)
    if not (3 <= len(summary.takeaways) <= 5):
        errors.append(f"Takeaway count {len(summary.takeaways)} outside range [3, 5]")

    # Each takeaway length
    for i, takeaway in enumerate(summary.takeaways):
        if not (50 <= len(takeaway) <= 150):
            errors.append(f"Takeaway {i+1} length {len(takeaway)} outside range [50, 150]")

    return ValidationResult(valid=len(errors) == 0, errors=errors)
```

### Quiz Validation
```python
def validate_quiz(quiz: Quiz, questions: List[QuizQuestion]) -> ValidationResult:
    errors = []

    # Question count (constitution)
    if not (5 <= len(questions) <= 7):
        errors.append(f"Question count {len(questions)} outside range [5, 7]")

    # Each question validation
    for i, q in enumerate(questions):
        if len(q.options) != 4:
            errors.append(f"Question {i+1} must have exactly 4 options")

        if not (0 <= q.correct_index <= 3):
            errors.append(f"Question {i+1} correct_index {q.correct_index} outside range [0, 3]")

        if not (50 <= len(q.question_text) <= 200):
            errors.append(f"Question {i+1} text length outside range [50, 200]")

    return ValidationResult(valid=len(errors) == 0, errors=errors)
```

---

## Storage Strategy

### Markdown Files
- **Location**: `/website/docs/`
- **Naming**: `{chapter_number:02d}-{slug}.md` (e.g., `01-physical-ai-intro.md`)
- **Format**: Docusaurus-compatible markdown with MDX for components
- **Version Control**: Git (tracked in repository)

### Database (Neon PostgreSQL)
- **Purpose**: Metadata, relationships, validation status, generation tracking
- **Connection**: Pooled connections via asyncpg (Python)
- **Migrations**: Alembic for schema versioning

### Vector Store (Qdrant)
- **Purpose**: Chapter embeddings for RAG (separate feature)
- **Content**: Chunked chapter text with metadata references
- **Note**: Population handled by separate RAG pipeline feature

---

## Next Steps

1. ✅ Data model complete - all entities, relationships, and validation rules defined
2. ⏳ Create contracts/content-generation-api.yaml (OpenAPI spec)
3. ⏳ Write quickstart.md for generation workflow
4. ⏳ Update plan.md with data model reference
5. ⏳ Proceed to `/sp.tasks` for implementation task breakdown
