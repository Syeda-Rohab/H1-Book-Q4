"""Initial schema for textbook content generation

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-12-10

Creates all tables for textbook content generation:
- generation_jobs: Tracks batch generation jobs
- chapters: Chapter metadata
- chapter_contents: Markdown file references
- summaries: AI-generated chapter summaries
- quizzes: Quiz collections per chapter
- quiz_questions: Individual quiz questions
- learning_boosters: Supplementary learning content
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM types
    job_status = postgresql.ENUM('pending', 'in_progress', 'completed', 'failed', name='job_status')
    job_status.create(op.get_bind())

    chapter_status = postgresql.ENUM('pending', 'generated', 'validated', 'published', 'failed', name='chapter_status')
    chapter_status.create(op.get_bind())

    validation_status = postgresql.ENUM('valid', 'invalid', 'pending_review', name='validation_status')
    validation_status.create(op.get_bind())

    booster_type = postgresql.ENUM('analogy', 'example', 'explanation', name='booster_type')
    booster_type.create(op.get_bind())

    question_difficulty = postgresql.ENUM('easy', 'medium', 'hard', name='question_difficulty')
    question_difficulty.create(op.get_bind())

    # 1. generation_jobs table
    op.create_table(
        'generation_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('started_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('status', job_status, nullable=False, server_default='pending'),
        sa.Column('chapters_completed', sa.Integer, nullable=False, server_default='0'),
        sa.Column('chapters_total', sa.Integer, nullable=False),
        sa.Column('errors', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('token_usage', sa.Integer, nullable=False, server_default='0'),
        sa.Column('model_used', sa.String(100), nullable=False),
        sa.CheckConstraint('chapters_completed <= chapters_total', name='check_chapters_completed'),
        sa.CheckConstraint('token_usage >= 0', name='check_token_usage')
    )
    op.create_index('idx_generation_jobs_status', 'generation_jobs', ['status'])
    op.create_index('idx_generation_jobs_started_at', 'generation_jobs', [sa.text('started_at DESC')])

    # 2. chapters table
    op.create_table(
        'chapters',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_number', sa.Integer, nullable=False, unique=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True),
        sa.Column('word_count', sa.Integer, nullable=False),
        sa.Column('reading_time_minutes', sa.Integer, nullable=False),
        sa.Column('status', chapter_status, nullable=False, server_default='pending'),
        sa.Column('validation_errors', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['job_id'], ['generation_jobs.id'], ondelete='CASCADE'),
        sa.CheckConstraint('chapter_number >= 1 AND chapter_number <= 8', name='check_chapter_number'),
        sa.CheckConstraint('word_count >= 800 AND word_count <= 1200', name='check_word_count'),
        sa.CheckConstraint('reading_time_minutes >= 5 AND reading_time_minutes <= 7', name='check_reading_time')
    )
    op.create_index('idx_chapters_job_id', 'chapters', ['job_id'])
    op.create_index('idx_chapters_number', 'chapters', ['chapter_number'])
    op.create_index('idx_chapters_status', 'chapters', ['status'])

    # 3. chapter_contents table
    op.create_table(
        'chapter_contents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('markdown_path', sa.String(500), nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=False),
        sa.Column('docusaurus_url', sa.String(500), nullable=False),
        sa.Column('stored_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE')
    )
    op.create_index('idx_chapter_contents_chapter_id', 'chapter_contents', ['chapter_id'])
    op.create_index('idx_chapter_contents_hash', 'chapter_contents', ['content_hash'])

    # 4. summaries table
    op.create_table(
        'summaries',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('takeaways', postgresql.JSONB, nullable=False),
        sa.Column('model_used', sa.String(100), nullable=False),
        sa.Column('validation_status', validation_status, nullable=False, server_default='pending_review'),
        sa.Column('generated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE')
    )
    op.create_index('idx_summaries_chapter_id', 'summaries', ['chapter_id'])
    op.create_index('idx_summaries_validation_status', 'summaries', ['validation_status'])

    # 5. quizzes table
    op.create_table(
        'quizzes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('total_questions', sa.Integer, nullable=False),
        sa.Column('model_used', sa.String(100), nullable=False),
        sa.Column('validation_status', validation_status, nullable=False, server_default='pending_review'),
        sa.Column('generated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.CheckConstraint('total_questions >= 5 AND total_questions <= 7', name='check_total_questions')
    )
    op.create_index('idx_quizzes_chapter_id', 'quizzes', ['chapter_id'])
    op.create_index('idx_quizzes_validation_status', 'quizzes', ['validation_status'])

    # 6. quiz_questions table
    op.create_table(
        'quiz_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('quiz_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question_number', sa.Integer, nullable=False),
        sa.Column('question_text', sa.Text, nullable=False),
        sa.Column('options', postgresql.JSONB, nullable=False),
        sa.Column('correct_index', sa.Integer, nullable=False),
        sa.Column('difficulty', question_difficulty, nullable=False),
        sa.Column('topic', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='CASCADE'),
        sa.CheckConstraint('correct_index >= 0 AND correct_index <= 3', name='check_correct_index')
    )
    op.create_index('idx_quiz_questions_quiz_id', 'quiz_questions', ['quiz_id'])
    op.create_index('idx_quiz_questions_difficulty', 'quiz_questions', ['difficulty'])

    # 7. learning_boosters table
    op.create_table(
        'learning_boosters',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('booster_type', booster_type, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('section_ref', sa.String(255), nullable=False),
        sa.Column('position', sa.Integer, nullable=False),
        sa.Column('model_used', sa.String(100), nullable=False),
        sa.Column('validation_status', validation_status, nullable=False, server_default='pending_review'),
        sa.Column('generated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.CheckConstraint('position >= 1 AND position <= 3', name='check_position')
    )
    op.create_index('idx_learning_boosters_chapter_id', 'learning_boosters', ['chapter_id'])
    op.create_index('idx_learning_boosters_type', 'learning_boosters', ['booster_type'])
    op.create_index('idx_learning_boosters_validation_status', 'learning_boosters', ['validation_status'])


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_index('idx_learning_boosters_validation_status', table_name='learning_boosters')
    op.drop_index('idx_learning_boosters_type', table_name='learning_boosters')
    op.drop_index('idx_learning_boosters_chapter_id', table_name='learning_boosters')
    op.drop_table('learning_boosters')

    op.drop_index('idx_quiz_questions_difficulty', table_name='quiz_questions')
    op.drop_index('idx_quiz_questions_quiz_id', table_name='quiz_questions')
    op.drop_table('quiz_questions')

    op.drop_index('idx_quizzes_validation_status', table_name='quizzes')
    op.drop_index('idx_quizzes_chapter_id', table_name='quizzes')
    op.drop_table('quizzes')

    op.drop_index('idx_summaries_validation_status', table_name='summaries')
    op.drop_index('idx_summaries_chapter_id', table_name='summaries')
    op.drop_table('summaries')

    op.drop_index('idx_chapter_contents_hash', table_name='chapter_contents')
    op.drop_index('idx_chapter_contents_chapter_id', table_name='chapter_contents')
    op.drop_table('chapter_contents')

    op.drop_index('idx_chapters_status', table_name='chapters')
    op.drop_index('idx_chapters_number', table_name='chapters')
    op.drop_index('idx_chapters_job_id', table_name='chapters')
    op.drop_table('chapters')

    op.drop_index('idx_generation_jobs_started_at', table_name='generation_jobs')
    op.drop_index('idx_generation_jobs_status', table_name='generation_jobs')
    op.drop_table('generation_jobs')

    # Drop ENUM types
    sa.Enum(name='question_difficulty').drop(op.get_bind())
    sa.Enum(name='booster_type').drop(op.get_bind())
    sa.Enum(name='validation_status').drop(op.get_bind())
    sa.Enum(name='chapter_status').drop(op.get_bind())
    sa.Enum(name='job_status').drop(op.get_bind())
