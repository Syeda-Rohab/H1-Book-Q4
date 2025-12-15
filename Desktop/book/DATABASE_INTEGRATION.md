# Database Integration TODO

This document tracks database integration work that needs to be completed for the backend API.

## Current Status

The backend structure is ready with models, services, and routes defined, but database integration is **not yet implemented**. The system currently works without a database for content generation.

## Pending Work

### 1. Database Configuration

**File:** `backend/src/database.py` (needs to be created)

Create database configuration module:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/textbook_db")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session():
    async with async_session_factory() as session:
        yield session
```

### 2. Update Content Routes

**File:** `backend/src/routes/content_routes.py`

**Line 31-39:** Replace placeholder `get_db_session()` with actual implementation:

```python
from backend.src.database import get_db_session

# Remove the placeholder function and use the one from database.py
```

### 3. Update Health Routes

**File:** `backend/src/routes/health_routes.py`

**Line 189-212:** Implement actual database health check:

```python
async def _check_database() -> bool:
    """Check database connectivity."""
    try:
        from backend.src.database import engine
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
```

### 4. Run Migrations

**Prerequisites:** Neon PostgreSQL database configured

```bash
# Set database URL
export DATABASE_URL="postgresql+asyncpg://user:pass@your-neon-db.neon.tech/textbook_db"

# Run migrations
cd backend
alembic upgrade head
```

### 5. Environment Configuration

**File:** `.env`

Add database configuration:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:pass@your-neon-db.neon.tech/textbook_db

# Optional: Database connection pool settings
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

## Database Schema

Already defined in `backend/src/models/`:

- **GenerationJob** - Tracks AI generation jobs
- **Chapter** - Chapter metadata
- **Summary** - Chapter summaries
- **Quiz** / **QuizQuestion** - Quiz data
- **LearningBooster** - Learning boosters (analogies, examples, explanations)

## Why Database is Optional for MVP

The current system works **without a database** because:

1. **Content generation is file-based** - Generated markdown files are written directly to `website/docs/`
2. **Docusaurus reads from files** - The frontend reads markdown files, not database
3. **No user data** - MVP has no authentication or user-specific data

**Database is needed for:**
- Multi-user support
- Generation job tracking
- Content versioning
- RAG pipeline (future)
- Usage analytics

## Migration Path

When ready to integrate database:

1. Set up Neon PostgreSQL database (free tier)
2. Create `backend/src/database.py` with connection config
3. Update `content_routes.py` and `health_routes.py`
4. Run Alembic migrations
5. Update generation scripts to persist to database
6. Test health endpoints
7. Deploy backend to Railway

## Estimated Effort

- Database setup: 30 minutes
- Code integration: 1-2 hours
- Testing: 1 hour
- **Total: 3-4 hours**

## Priority

**Low** - Database integration is not blocking for:
- Content generation
- Docusaurus website
- GitHub Pages deployment
- MVP launch

**High** - Required for:
- User authentication
- Generation job tracking
- RAG chatbot (Phase 2)
- Production backend deployment

## Notes

- All database models are already defined and ready
- Migration files exist in `backend/alembic/versions/`
- Free tier Neon PostgreSQL is sufficient for MVP
- Connection pooling configured for Railway deployment
