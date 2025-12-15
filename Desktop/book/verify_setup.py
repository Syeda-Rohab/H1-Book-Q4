#!/usr/bin/env python3
"""Verify complete system setup - run this to check if everything is ready."""

import os
import sys
from pathlib import Path

# Windows compatibility
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def check_api_key():
    """Check if API key is set."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        print("   Run: export ANTHROPIC_API_KEY='your-key'")
        return False

    if len(api_key) < 50:
        print("❌ API key looks incomplete (too short)")
        return False

    print(f"✅ API key set ({len(api_key)} chars)")
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    required = ['anthropic', 'pydantic']
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)

    return len(missing) == 0

def check_api_credits():
    """Test if account has credits."""
    try:
        import anthropic
        client = anthropic.Anthropic()

        # Try a minimal API call
        response = client.messages.create(
            model='claude-3-5-haiku-20241022',
            max_tokens=10,
            messages=[{'role': 'user', 'content': 'Hi'}]
        )

        print("✅ API credits available - Ready to generate!")
        return True

    except anthropic.BadRequestError as e:
        if "credit balance is too low" in str(e):
            print("❌ No credits in account")
            print("   Visit: https://console.anthropic.com/settings/billing")
            print("   Add $5-10 to generate content (~$0.23 needed)")
            return False
        else:
            print(f"❌ API error: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_files():
    """Check if all required files exist."""
    required_files = [
        'agents/content_generator/chapter_generator.py',
        'agents/content_generator/summary_generator.py',
        'agents/content_generator/quiz_generator.py',
        'agents/content_generator/booster_generator.py',
        'scripts/generate_chapters.py',
        'scripts/generate_summaries.py',
        'scripts/generate_quizzes.py',
        'scripts/generate_boosters.py',
        'website/src/components/ChapterQuiz.tsx',
        'website/src/components/LearningBooster.tsx',
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False

    return all_exist

def main():
    print("="*70)
    print("AI-NATIVE TEXTBOOK SYSTEM VERIFICATION")
    print("="*70)
    print()

    print("1. Checking API Key...")
    api_key_ok = check_api_key()
    print()

    print("2. Checking Python Dependencies...")
    deps_ok = check_dependencies()
    print()

    print("3. Checking Required Files...")
    files_ok = check_files()
    print()

    print("4. Testing API Credits...")
    credits_ok = check_api_credits()
    print()

    print("="*70)
    print("SUMMARY")
    print("="*70)

    all_checks = [
        ("API Key", api_key_ok),
        ("Dependencies", deps_ok),
        ("Files", files_ok),
        ("Credits", credits_ok),
    ]

    for name, status in all_checks:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {name}")

    print()

    if all(status for _, status in all_checks):
        print("🎉 ALL CHECKS PASSED - Ready to generate!")
        print()
        print("Run these commands to generate your textbook:")
        print()
        print("  PYTHONPATH=. python scripts/generate_chapters.py")
        print("  PYTHONPATH=. python scripts/generate_summaries.py")
        print("  PYTHONPATH=. python scripts/generate_quizzes.py")
        print("  PYTHONPATH=. python scripts/generate_boosters.py")
        return 0
    else:
        print("⚠️  Some checks failed - follow instructions above to fix")
        return 1

if __name__ == "__main__":
    sys.exit(main())
