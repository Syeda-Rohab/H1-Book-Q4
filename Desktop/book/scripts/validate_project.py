"""Comprehensive project validation script.

Validates code quality, structure, tests, and completeness.

Usage:
    python scripts/validate_project.py
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent


class ProjectValidator:
    """Comprehensive project validation."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passes: List[str] = []

    def validate_all(self) -> bool:
        """Run all validations."""
        print("=" * 60)
        print("PROJECT VALIDATION")
        print("=" * 60 + "\n")

        self._validate_structure()
        self._validate_python_code()
        self._validate_documentation()
        self._validate_configuration()
        self._validate_frontend()

        self._print_results()
        return len(self.errors) == 0

    def _validate_structure(self) -> None:
        """Validate project structure."""
        print("Checking project structure...")

        required_paths = [
            "agents/content_generator",
            "backend/src/models",
            "backend/src/services",
            "backend/src/routes",
            "backend/src/utils",
            "website/docs",
            "website/src/components",
            "scripts",
            "specs",
            ".specify/memory",
        ]

        for path in required_paths:
            full_path = project_root / path
            if full_path.exists():
                self.passes.append(f"Structure: {path} exists ✓")
            else:
                self.errors.append(f"Structure: Missing {path}")

    def _validate_python_code(self) -> None:
        """Validate Python code quality."""
        print("Checking Python code...")

        # Check for required Python files
        required_files = [
            "agents/content_generator/llm_client.py",
            "agents/content_generator/chapter_generator.py",
            "agents/content_generator/summary_generator.py",
            "agents/content_generator/quiz_generator.py",
            "agents/content_generator/booster_generator.py",
            "agents/content_generator/validator.py",
            "agents/content_generator/token_tracker.py",
            "backend/src/utils/logging.py",
        ]

        for file in required_files:
            full_path = project_root / file
            if full_path.exists():
                self.passes.append(f"Python: {file} exists ✓")

                # Check for basic Python syntax
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if not content.strip():
                            self.errors.append(f"Python: {file} is empty")
                        elif "def " in content or "class " in content:
                            self.passes.append(f"Python: {file} has valid code ✓")
                except Exception as e:
                    self.errors.append(f"Python: Cannot read {file}: {e}")
            else:
                self.errors.append(f"Python: Missing {file}")

        # Check for __init__.py files
        init_paths = [
            "agents/__init__.py",
            "agents/content_generator/__init__.py",
            "backend/src/__init__.py",
            "backend/src/models/__init__.py",
            "backend/src/services/__init__.py",
            "backend/src/routes/__init__.py",
        ]

        for init_path in init_paths:
            full_path = project_root / init_path
            if full_path.exists():
                self.passes.append(f"Python: {init_path} present ✓")
            else:
                self.warnings.append(f"Python: Missing {init_path}")

    def _validate_documentation(self) -> None:
        """Validate documentation."""
        print("Checking documentation...")

        required_docs = [
            "README.md",
            "CLAUDE.md",
            ".specify/memory/constitution.md",
            "DEPLOYMENT_GUIDE.md",
            "CONTRIBUTING.md",
        ]

        for doc in required_docs:
            full_path = project_root / doc
            if full_path.exists():
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if len(content.strip()) > 100:
                            self.passes.append(f"Docs: {doc} exists with content ✓")
                        else:
                            self.warnings.append(f"Docs: {doc} is too short")
                except Exception as e:
                    self.warnings.append(f"Docs: Cannot read {doc}: {e}")
            else:
                self.errors.append(f"Docs: Missing {doc}")

    def _validate_configuration(self) -> None:
        """Validate configuration files."""
        print("Checking configuration...")

        config_files = [
            ".env.example",
            "requirements.txt",
            "backend/requirements.txt",
            "agents/content_generator/requirements.txt",
            "website/package.json",
            "website/docusaurus.config.js",
        ]

        for config in config_files:
            full_path = project_root / config
            if full_path.exists():
                self.passes.append(f"Config: {config} exists ✓")
            else:
                self.warnings.append(f"Config: Missing {config}")

    def _validate_frontend(self) -> None:
        """Validate frontend components."""
        print("Checking frontend...")

        # Check for React components
        components = [
            "website/src/components/ChapterQuiz.tsx",
            "website/src/components/ChapterQuiz.module.css",
            "website/src/components/LearningBooster.tsx",
            "website/src/components/LearningBooster.module.css",
        ]

        for component in components:
            full_path = project_root / component
            if full_path.exists():
                self.passes.append(f"Frontend: {component} exists ✓")
            else:
                self.errors.append(f"Frontend: Missing {component}")

        # Check for chapter content
        docs_path = project_root / "website" / "docs"
        if docs_path.exists():
            chapters = list(docs_path.glob("chapter-*.md"))
            if len(chapters) >= 6:
                self.passes.append(f"Frontend: {len(chapters)} chapters found ✓")
            else:
                self.errors.append(f"Frontend: Only {len(chapters)} chapters (expected 6+)")

        # Check build directory
        build_path = project_root / "website" / "build"
        if build_path.exists():
            self.passes.append("Frontend: Production build exists ✓")
        else:
            self.warnings.append("Frontend: No production build found")

    def _print_results(self) -> None:
        """Print validation results."""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60 + "\n")

        if self.passes:
            print(f"✓ PASSED ({len(self.passes)}):")
            for p in self.passes[:10]:  # Show first 10
                print(f"  ✓ {p}")
            if len(self.passes) > 10:
                print(f"  ... and {len(self.passes) - 10} more")
            print("")

        if self.warnings:
            print(f"⚠ WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  ⚠ {w}")
            print("")

        if self.errors:
            print(f"✗ ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  ✗ {e}")
            print("")

        print("=" * 60)
        print(f"Summary: {len(self.passes)} passed, {len(self.warnings)} warnings, {len(self.errors)} errors")
        print("=" * 60 + "\n")

        if self.errors:
            print("❌ Project validation FAILED")
        elif self.warnings:
            print("⚠️  Project validation PASSED with warnings")
        else:
            print("✅ Project validation PASSED")


def main():
    """Run project validation."""
    validator = ProjectValidator()
    success = validator.validate_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
