#!/usr/bin/env python3
"""Test which Claude models are accessible."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(".env")

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: No API key found")
    exit(1)

client = Anthropic(api_key=api_key)

# Test different model names
models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
]

print("Testing models...\n")

for model in models_to_test:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"[OK] {model} - WORKS")
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"[FAIL] {model} - {error_msg}")

print("\nDone!")
