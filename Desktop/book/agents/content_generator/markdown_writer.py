"""Markdown file writer for Docusaurus content.

Writes generated chapter content to markdown files in the Docusaurus docs directory
with proper frontmatter and formatting.

Based on tasks.md: T031 - Markdown file writer
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MarkdownMetadata:
    """Metadata for Docusaurus frontmatter.

    Attributes:
        sidebar_position: Position in sidebar (1-8 for chapters)
        sidebar_label: Label shown in sidebar
        title: Page title
        description: Page description (for SEO)
        keywords: List of keywords for SEO
    """

    sidebar_position: int
    sidebar_label: str
    title: str
    description: str
    keywords: list[str]


class MarkdownWriter:
    """Writes chapter content to Docusaurus-compatible markdown files.

    Features:
    - Generates Docusaurus frontmatter (YAML)
    - Creates proper directory structure
    - Ensures UTF-8 encoding
    - Validates output paths
    - Tracks file metadata (path, hash, URL)

    Based on tasks.md: T031 - Markdown file writer
    """

    def __init__(self, docs_directory: str = "website/docs"):
        """Initialize the markdown writer.

        Args:
            docs_directory: Path to Docusaurus docs directory (default: website/docs)
        """
        self.docs_directory = Path(docs_directory)
        logger.info(f"MarkdownWriter initialized (docs_dir={self.docs_directory})")

    def write_chapter(
        self,
        chapter_number: int,
        title: str,
        slug: str,
        content: str,
        metadata: Optional[MarkdownMetadata] = None,
    ) -> dict:
        """Write a chapter to a markdown file.

        Args:
            chapter_number: Chapter number (1-8)
            title: Chapter title
            slug: URL-friendly slug (e.g., 'physical-ai-intro')
            content: Chapter markdown content
            metadata: Optional Docusaurus metadata (auto-generated if not provided)

        Returns:
            Dictionary with file path, docusaurus URL, and content hash

        Raises:
            ValueError: If chapter_number is invalid
            OSError: If file write fails
        """
        if not (1 <= chapter_number <= 8):
            raise ValueError(f"Chapter number must be 1-8 (got {chapter_number})")

        logger.info(f"Writing chapter {chapter_number}: {title}")

        # Generate metadata if not provided
        if metadata is None:
            metadata = self._generate_default_metadata(chapter_number, title, slug)

        # Generate frontmatter
        frontmatter = self._generate_frontmatter(metadata)

        # Combine frontmatter and content
        full_content = f"{frontmatter}\n\n{content}"

        # Generate file path
        filename = f"chapter-{chapter_number:02d}-{slug}.md"
        file_path = self.docs_directory / filename

        # Ensure docs directory exists
        self.docs_directory.mkdir(parents=True, exist_ok=True)

        # Write file
        try:
            file_path.write_text(full_content, encoding="utf-8")
            logger.info(f"Chapter {chapter_number} written to {file_path}")
        except OSError as e:
            logger.error(f"Failed to write chapter {chapter_number}: {e}")
            raise

        # Generate Docusaurus URL
        docusaurus_url = f"/docs/{slug}"

        # Calculate content hash
        import hashlib
        content_hash = hashlib.sha256(full_content.encode("utf-8")).hexdigest()

        return {
            "file_path": str(file_path),
            "docusaurus_url": docusaurus_url,
            "content_hash": content_hash,
            "filename": filename,
        }

    def write_intro_page(
        self,
        title: str,
        description: str,
        chapters: list[dict],
    ) -> dict:
        """Write the Docusaurus intro/homepage for the textbook.

        Args:
            title: Textbook title
            description: Textbook description
            chapters: List of chapter dictionaries with 'number', 'title', 'slug'

        Returns:
            Dictionary with file path and URL

        Raises:
            OSError: If file write fails
        """
        logger.info("Writing intro page")

        # Generate frontmatter
        frontmatter = """---
sidebar_position: 1
sidebar_label: Introduction
title: Welcome to the Textbook
description: AI-Native Textbook on Physical AI & Humanoid Robotics
---
"""

        # Generate intro content
        intro_content = f"""# {title}

{description}

## About This Textbook

This is an **AI-native textbook** that leverages artificial intelligence to deliver high-quality educational content on Physical AI and Humanoid Robotics. Each chapter is carefully generated and validated to ensure:

- **Clarity and Accessibility**: Written for learners with basic technical knowledge
- **Optimal Reading Time**: Each chapter is 5-7 minutes (800-1200 words)
- **Interactive Learning**: Includes summaries, quizzes, and learning boosters
- **Mobile-Friendly**: Optimized for reading on any device

## Table of Contents

"""

        # Add chapter list
        for chapter in chapters:
            intro_content += f"- [Chapter {chapter['number']}: {chapter['title']}](./{chapter['slug']})\n"

        intro_content += """
## How to Use This Textbook

1. **Read sequentially**: Chapters build on each other progressively
2. **Review summaries**: Each chapter ends with key takeaways
3. **Test yourself**: Take quizzes to assess your understanding
4. **Explore boosters**: Use learning aids (analogies, examples) for difficult concepts

## Getting Started

Start with [Chapter 1: Introduction to Physical AI](./physical-ai-intro) to begin your learning journey!

---

*Generated with AI • Last updated: {date}*
""".format(date=datetime.now().strftime("%Y-%m-%d"))

        # Combine frontmatter and content
        full_content = f"{frontmatter}\n{intro_content}"

        # Write to intro.md
        intro_path = self.docs_directory / "intro.md"

        try:
            self.docs_directory.mkdir(parents=True, exist_ok=True)
            intro_path.write_text(full_content, encoding="utf-8")
            logger.info(f"Intro page written to {intro_path}")
        except OSError as e:
            logger.error(f"Failed to write intro page: {e}")
            raise

        return {
            "file_path": str(intro_path),
            "docusaurus_url": "/docs/intro",
            "filename": "intro.md",
        }

    def _generate_default_metadata(
        self, chapter_number: int, title: str, slug: str
    ) -> MarkdownMetadata:
        """Generate default metadata for a chapter.

        Args:
            chapter_number: Chapter number
            title: Chapter title
            slug: URL slug

        Returns:
            MarkdownMetadata with defaults
        """
        # Extract keywords from title (simple approach)
        keywords = [word.lower() for word in title.split() if len(word) > 3]
        keywords.extend(["physical ai", "robotics", "humanoid robots"])

        return MarkdownMetadata(
            sidebar_position=chapter_number + 1,  # +1 because intro.md is position 1
            sidebar_label=f"Chapter {chapter_number}",
            title=title,
            description=f"Chapter {chapter_number} of the AI-Native Textbook on Physical AI and Humanoid Robotics",
            keywords=keywords,
        )

    def _generate_frontmatter(self, metadata: MarkdownMetadata) -> str:
        """Generate YAML frontmatter for Docusaurus.

        Args:
            metadata: Markdown metadata

        Returns:
            YAML frontmatter string (with --- delimiters)
        """
        # Format keywords as YAML array
        keywords_yaml = "[" + ", ".join(f'"{k}"' for k in metadata.keywords) + "]"

        frontmatter = f"""---
sidebar_position: {metadata.sidebar_position}
sidebar_label: {metadata.sidebar_label}
title: {metadata.title}
description: {metadata.description}
keywords: {keywords_yaml}
---"""

        return frontmatter

    def validate_docs_directory(self) -> bool:
        """Validate that the docs directory exists and is writable.

        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if directory exists
            if not self.docs_directory.exists():
                logger.warning(f"Docs directory does not exist: {self.docs_directory}")
                return False

            # Check if writable (try to create a test file)
            test_file = self.docs_directory / ".write_test"
            test_file.write_text("test", encoding="utf-8")
            test_file.unlink()

            logger.info(f"Docs directory is valid and writable: {self.docs_directory}")
            return True

        except (OSError, PermissionError) as e:
            logger.error(f"Docs directory is not writable: {e}")
            return False

    def get_chapter_file_path(self, chapter_number: int, slug: str) -> Path:
        """Get the file path for a chapter.

        Args:
            chapter_number: Chapter number
            slug: URL slug

        Returns:
            Path to the chapter markdown file
        """
        filename = f"chapter-{chapter_number:02d}-{slug}.md"
        return self.docs_directory / filename

    def chapter_file_exists(self, chapter_number: int, slug: str) -> bool:
        """Check if a chapter file already exists.

        Args:
            chapter_number: Chapter number
            slug: URL slug

        Returns:
            True if file exists
        """
        file_path = self.get_chapter_file_path(chapter_number, slug)
        return file_path.exists()

    def append_summary_to_chapter(
        self,
        chapter_number: int,
        slug: str,
        takeaways: list[str],
    ) -> dict:
        """Append a summary section to an existing chapter file.

        Args:
            chapter_number: Chapter number
            slug: URL slug
            takeaways: List of 3-5 key takeaway strings

        Returns:
            Dictionary with file path and updated content hash

        Raises:
            FileNotFoundError: If chapter file doesn't exist
            OSError: If file read/write fails
        """
        logger.info(f"Appending summary to chapter {chapter_number}")

        # Get chapter file path
        file_path = self.get_chapter_file_path(chapter_number, slug)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Chapter file not found: {file_path}. "
                f"Generate the chapter first before adding a summary."
            )

        # Read existing content
        try:
            existing_content = file_path.read_text(encoding="utf-8")
        except OSError as e:
            logger.error(f"Failed to read chapter {chapter_number}: {e}")
            raise

        # Generate summary section
        summary_section = self._generate_summary_section(takeaways)

        # Append summary to content
        updated_content = f"{existing_content}\n\n{summary_section}"

        # Write updated content
        try:
            file_path.write_text(updated_content, encoding="utf-8")
            logger.info(f"Summary appended to chapter {chapter_number} at {file_path}")
        except OSError as e:
            logger.error(f"Failed to write updated chapter {chapter_number}: {e}")
            raise

        # Calculate updated content hash
        import hashlib
        content_hash = hashlib.sha256(updated_content.encode("utf-8")).hexdigest()

        return {
            "file_path": str(file_path),
            "content_hash": content_hash,
            "takeaways_count": len(takeaways),
        }

    def _generate_summary_section(self, takeaways: list[str]) -> str:
        """Generate a formatted summary section for a chapter.

        Args:
            takeaways: List of takeaway strings

        Returns:
            Formatted markdown summary section
        """
        summary = "## Chapter Summary\n\n"
        summary += "**Key Takeaways:**\n\n"

        for i, takeaway in enumerate(takeaways, start=1):
            # Add takeaways as a numbered list
            summary += f"{i}. {takeaway}\n"

        summary += "\n---\n\n"
        summary += f"*Summary generated on {datetime.now().strftime('%Y-%m-%d')}*"

        return summary

    def append_quiz_to_chapter(self, chapter_number: int, slug: str, questions: list[dict]) -> dict:
        """Append quiz to chapter file (T051)."""
        logger.info(f"Appending quiz to chapter {chapter_number}")
        file_path = self.get_chapter_file_path(chapter_number, slug)
        if not file_path.exists():
            raise FileNotFoundError(f"Chapter file not found: {file_path}")
        existing_content = file_path.read_text(encoding="utf-8")
        import json
        quiz_data = json.dumps(questions, indent=2)
        quiz_section = f"\n\n## Test Your Knowledge\n\nimport ChapterQuiz from '@site/src/components/ChapterQuiz';\n\n<ChapterQuiz questions={{{quiz_data}}} />\n\n---\n\n*Quiz generated on {datetime.now().strftime('%Y-%m-%d')}*"
        updated_content = existing_content + quiz_section
        file_path.write_text(updated_content, encoding="utf-8")
        import hashlib
        return {"file_path": str(file_path), "content_hash": hashlib.sha256(updated_content.encode("utf-8")).hexdigest(), "questions_count": len(questions)}

    def embed_boosters_in_chapter(self, chapter_number: int, slug: str, boosters: list[dict]) -> dict:
        """Embed learning boosters in chapter (T061)."""
        logger.info(f"Embedding boosters in chapter {chapter_number}")
        file_path = self.get_chapter_file_path(chapter_number, slug)
        if not file_path.exists(): raise FileNotFoundError(f"Chapter not found: {file_path}")
        content = file_path.read_text(encoding="utf-8")

        # Add import once at the top (after frontmatter)
        if "import LearningBooster" not in content:
            # Find the end of frontmatter
            parts = content.split('---\n', 2)
            if len(parts) >= 3:
                content = f"{parts[0]}---\n{parts[1]}---\n\nimport LearningBooster from '@site/src/components/LearningBooster';\n\n{parts[2]}"

        sections = content.split('\n## ')
        if len(sections) < 3: logger.warning("Not enough sections"); return {"file_path": str(file_path), "boosters_count": 0}
        for i, booster in enumerate(boosters[:3]):
            section_idx = min(i + 2, len(sections) - 1)
            # Only add the component, not the import
            booster_mdx = f"\n\n<LearningBooster type=\"{booster['booster_type']}\" content=\"{booster['content']}\" />\n\n"
            sections[section_idx] += booster_mdx
        updated = '\n## '.join(sections)
        file_path.write_text(updated, encoding="utf-8")
        import hashlib
        return {"file_path": str(file_path), "content_hash": hashlib.sha256(updated.encode("utf-8")).hexdigest(), "boosters_count": len(boosters)}
