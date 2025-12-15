#!/usr/bin/env python3
"""Fix duplicate LearningBooster imports in chapter files."""
from pathlib import Path
import re

docs_dir = Path("website/docs")
chapter_files = list(docs_dir.glob("chapter-*.md"))

for file_path in chapter_files:
    print(f"Fixing {file_path.name}...")

    content = file_path.read_text(encoding="utf-8")

    # Count how many times the import appears
    import_count = content.count("import LearningBooster")

    if import_count > 1:
        print(f"  Found {import_count} imports, removing duplicates...")

        # Split by the import statement
        parts = content.split("import LearningBooster from '@site/src/components/LearningBooster';")

        # Keep only the first occurrence (after frontmatter)
        # The first part is everything before the first import
        # The remaining parts should just be the content after each import

        # Join with empty string for all but the first import
        fixed = parts[0] + "import LearningBooster from '@site/src/components/LearningBooster';" + "".join(parts[1:])

        file_path.write_text(fixed, encoding="utf-8")
        print(f"  Fixed! Reduced to 1 import.")
    else:
        print(f"  OK ({import_count} import)")

print("\nDone!")
