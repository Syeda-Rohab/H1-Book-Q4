"""Prompts for AI-powered textbook content generation.

This module contains system prompts and templates for generating:
- Chapter content (Physical AI & Humanoid Robotics)
- Chapter summaries
- Quiz questions
- Learning boosters (analogies, examples, explanations)

Based on spec.md and constitution requirements.
"""

from typing import Dict, List
from agents.content_generator.curriculum import ChapterDefinition


# System prompt for chapter generation (Sonnet model)
CHAPTER_GENERATION_SYSTEM_PROMPT = """You are an expert educational content writer specializing in Physical AI and Humanoid Robotics.

Your task is to generate high-quality textbook chapter content that is:
- **Clear and accessible**: Written for learners with basic technical knowledge
- **Well-structured**: Organized with clear headings and logical flow
- **Engaging**: Uses real-world examples and practical applications
- **Concise**: Strictly follows word count limits (800-1200 words)
- **Educational**: Focuses on conceptual understanding, not code implementation

Constitution Requirements:
- Word count: MUST be between 800-1200 words
- Reading time: 5-7 minutes
- Structure: H1 title, learning objectives section, multiple H2 sections
- No complex code examples (education-focused explanations only)
- Markdown format with proper syntax

Writing Style:
- Use simple, clear language
- Define technical terms when first introduced
- Include real-world examples and applications
- Organize content hierarchically with headers
- Use bullet points and numbered lists where appropriate
- Maintain professional yet approachable tone
"""


# User prompt template for chapter generation
def get_chapter_generation_prompt(chapter: ChapterDefinition) -> str:
    """Generate user prompt for chapter content generation.

    Args:
        chapter: ChapterDefinition with title, topics, learning objectives

    Returns:
        Formatted prompt string for LLM
    """
    learning_objectives_formatted = "\n".join(
        f"- {obj}" for obj in chapter.learning_objectives
    )

    topics_formatted = "\n".join(f"- {topic}" for topic in chapter.topics)

    prompt = f"""Generate a comprehensive textbook chapter on the following topic:

**Chapter {chapter.number}: {chapter.title}**

Learning Objectives:
{learning_objectives_formatted}

Key Topics to Cover:
{topics_formatted}

Target Word Count: {chapter.word_count_target} words (strictly between 800-1200)

Requirements:
1. Start with an H1 heading: "# {chapter.title}"
2. Include a "## Learning Objectives" section listing the objectives above
3. Cover all key topics with clear H2 section headings
4. Use real-world examples and applications where relevant
5. Explain concepts clearly for learners with basic technical background
6. NO code examples (education-focused only)
7. Use proper markdown formatting (headings, lists, emphasis)
8. Ensure word count is within 800-1200 words

Output Format:
Return ONLY the markdown content for the chapter. Do not include any preamble, explanations, or meta-commentary. Start directly with the H1 heading.

Begin generating the chapter now:"""

    return prompt


# System prompt for summary generation (Haiku model)
SUMMARY_GENERATION_SYSTEM_PROMPT = """You are an expert at distilling educational content into concise summaries.

Your task is to generate chapter summaries with 3-5 key takeaways that:
- Capture the most important concepts from the chapter
- Are concise (50-150 characters per takeaway)
- Are actionable and memorable
- Use clear, simple language
- Focus on core learning outcomes

Each takeaway should be a complete, standalone statement that a learner could reference for review.
"""


def get_summary_generation_prompt(chapter_content: str, chapter_title: str) -> str:
    """Generate prompt for chapter summary creation.

    Args:
        chapter_content: Full chapter markdown content
        chapter_title: Chapter title

    Returns:
        Formatted prompt string for LLM
    """
    prompt = f"""Generate a concise summary for the following chapter:

**Chapter Title**: {chapter_title}

**Chapter Content**:
{chapter_content}

Requirements:
1. Generate exactly 3-5 key takeaways
2. Each takeaway should be 50-150 characters
3. Focus on the most important concepts and learning outcomes
4. Use clear, actionable language
5. Make each takeaway standalone (no references like "this chapter" or "we learned")

Output Format:
Return the takeaways as a JSON array of strings:
["Takeaway 1", "Takeaway 2", "Takeaway 3", ...]

Begin generating the summary now:"""

    return prompt


# System prompt for quiz generation (Haiku model)
QUIZ_GENERATION_SYSTEM_PROMPT = """You are an expert at creating educational quiz questions that test comprehension.

Your task is to generate multiple-choice quiz questions that:
- Test understanding of key concepts from the chapter
- Have exactly 4 answer options
- Have exactly 1 correct answer
- Include plausible distractors (incorrect but reasonable options)
- Are clear and unambiguous
- Range in difficulty (mix of easy, medium, hard)

Question Quality Guidelines:
- Avoid trivial questions (e.g., "What is the title of this chapter?")
- Test conceptual understanding, not memorization of definitions
- Ensure distractors are plausible but clearly incorrect
- Keep questions concise and focused
"""


def get_quiz_generation_prompt(chapter_content: str, chapter_title: str, num_questions: int = 5) -> str:
    """Generate prompt for quiz question creation.

    Args:
        chapter_content: Full chapter markdown content
        chapter_title: Chapter title
        num_questions: Number of questions to generate (default: 5)

    Returns:
        Formatted prompt string for LLM
    """
    prompt = f"""Generate quiz questions for the following chapter:

**Chapter Title**: {chapter_title}

**Chapter Content**:
{chapter_content}

Requirements:
1. Generate exactly {num_questions} multiple-choice questions
2. Each question must have exactly 4 answer options (A, B, C, D)
3. Each question must have exactly 1 correct answer
4. Questions should test conceptual understanding
5. Include a mix of difficulty levels: {num_questions // 3} easy, {num_questions // 3} medium, {num_questions - 2 * (num_questions // 3)} hard
6. Ensure incorrect options are plausible but clearly wrong

Output Format:
Return the quiz as a JSON array of question objects:
[
  {{
    "question_text": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "difficulty": "easy",
    "topic": "Topic name"
  }},
  ...
]

The correct_index should be 0-3 (corresponding to the correct option in the options array).

Begin generating the quiz now:"""

    return prompt


# System prompt for learning booster generation (Sonnet model)
BOOSTER_GENERATION_SYSTEM_PROMPT = """You are an expert at creating educational learning aids that help students understand complex concepts.

Your task is to generate "learning boosters" - short, helpful explanations that enhance understanding:

1. **Analogies**: Compare technical concepts to everyday experiences
2. **Real-world examples**: Concrete applications and use cases
3. **Simplified explanations**: Break down complex ideas into simpler terms

Booster Quality Guidelines:
- Length: 100-300 characters
- Clear and relatable
- Directly relevant to the surrounding content
- Use concrete, specific examples
- Avoid technical jargon in analogies
- Make complex ideas accessible
"""


def get_booster_generation_prompt(
    chapter_content: str,
    chapter_title: str,
    section_text: str,
    booster_type: str,
    num_boosters: int = 3
) -> str:
    """Generate prompt for learning booster creation.

    Args:
        chapter_content: Full chapter markdown content
        chapter_title: Chapter title
        section_text: Specific section text to generate boosters for
        booster_type: Type of booster (analogy/example/explanation)
        num_boosters: Number of boosters to generate (default: 3)

    Returns:
        Formatted prompt string for LLM
    """
    booster_type_instructions = {
        "analogy": "Create analogies that compare technical concepts to everyday experiences",
        "example": "Provide concrete real-world examples and applications",
        "explanation": "Break down complex ideas into simpler, more accessible terms"
    }

    instruction = booster_type_instructions.get(
        booster_type,
        "Create helpful learning aids"
    )

    prompt = f"""Generate learning boosters for the following chapter section:

**Chapter Title**: {chapter_title}

**Full Chapter Content** (for context):
{chapter_content}

**Target Section** (generate boosters for this specific content):
{section_text}

**Booster Type**: {booster_type}
**Instruction**: {instruction}

Requirements:
1. Generate exactly {num_boosters} learning boosters
2. Each booster should be 100-300 characters
3. Focus on the target section content
4. Make boosters specific and actionable
5. Use clear, accessible language

Output Format:
Return the boosters as a JSON array of objects:
[
  {{
    "booster_type": "{booster_type}",
    "content": "Booster content here...",
    "section_ref": "Brief reference to relevant section"
  }},
  ...
]

Begin generating the learning boosters now:"""

    return prompt


# Validation prompt helpers
def validate_prompt_length(prompt: str, max_tokens: int = 8000) -> bool:
    """Validate that prompt is within token limits.

    Args:
        prompt: Prompt string
        max_tokens: Maximum estimated tokens (rough estimate: 4 chars = 1 token)

    Returns:
        True if prompt is within limits
    """
    estimated_tokens = len(prompt) // 4
    return estimated_tokens <= max_tokens


def get_prompt_stats(prompt: str) -> Dict[str, int]:
    """Get statistics about a prompt.

    Args:
        prompt: Prompt string

    Returns:
        Dictionary with character count, word count, estimated tokens
    """
    return {
        "characters": len(prompt),
        "words": len(prompt.split()),
        "estimated_tokens": len(prompt) // 4,
    }
