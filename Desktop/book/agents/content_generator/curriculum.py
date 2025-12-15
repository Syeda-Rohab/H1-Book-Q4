"""Curriculum definition for Physical AI & Humanoid Robotics textbook.

This module defines the chapter structure, topics, and learning objectives
for the AI-powered textbook generation system.

Based on research findings in specs/005-textbook-generation/research.md
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ChapterDefinition:
    """Definition of a single textbook chapter.

    Attributes:
        number: Sequential chapter number (1-8)
        title: Chapter title
        slug: URL-friendly slug for Docusaurus routing
        learning_objectives: List of 3-5 learning objectives
        topics: List of key topics to cover
        word_count_target: Target word count (must be 800-1200 per constitution)
        priority: Priority tier (P1=MVP core, P2=extended, P3=optional)
    """

    number: int
    title: str
    slug: str
    learning_objectives: List[str]
    topics: List[str]
    word_count_target: int
    priority: str

    def __post_init__(self):
        """Validate chapter definition."""
        if not (800 <= self.word_count_target <= 1200):
            raise ValueError(
                f"word_count_target must be 800-1200 (got {self.word_count_target})"
            )
        if self.priority not in ["P1", "P2", "P3"]:
            raise ValueError(f"priority must be P1, P2, or P3 (got {self.priority})")


# Textbook curriculum definition
# Based on research.md: Research Task 4 - Curriculum Design
CURRICULUM: List[ChapterDefinition] = [
    # MVP Core Chapters (P1) - Required for initial release
    ChapterDefinition(
        number=1,
        title="Introduction to Physical AI",
        slug="physical-ai-intro",
        learning_objectives=[
            "Define Physical AI and distinguish from traditional AI",
            "Understand the role of embodiment in intelligence",
            "Identify real-world applications of Physical AI",
        ],
        topics=[
            "What is Physical AI",
            "History and evolution",
            "Embodied intelligence",
            "Applications (industrial robots, drones, autonomous vehicles)",
            "Key challenges and opportunities",
        ],
        word_count_target=1000,
        priority="P1",
    ),
    ChapterDefinition(
        number=2,
        title="Humanoid Robotics Fundamentals",
        slug="humanoid-robotics-fundamentals",
        learning_objectives=[
            "Explain the motivation for humanoid form factors",
            "Describe key components of humanoid robots",
            "Understand design challenges and trade-offs",
        ],
        topics=[
            "Why humanoid robots",
            "Anatomy (torso, limbs, head)",
            "Degrees of freedom (DOF)",
            "Balance and stability",
            "Examples (Atlas, Optimus, Digit)",
        ],
        word_count_target=1100,
        priority="P1",
    ),
    ChapterDefinition(
        number=3,
        title="Sensors and Perception",
        slug="sensors-perception",
        learning_objectives=[
            "Identify sensor types used in robotics",
            "Explain sensor fusion principles",
            "Understand perception pipelines",
        ],
        topics=[
            "Vision (cameras, lidar)",
            "Tactile sensors",
            "IMUs (Inertial Measurement Units)",
            "Proprioception",
            "Sensor fusion",
            "Perception for navigation",
        ],
        word_count_target=1000,
        priority="P1",
    ),
    ChapterDefinition(
        number=4,
        title="Actuators and Motion",
        slug="actuators-motion",
        learning_objectives=[
            "Describe actuator technologies",
            "Explain motion control principles",
            "Understand gait generation for humanoid robots",
        ],
        topics=[
            "Motors (servo, stepper)",
            "Hydraulics",
            "Pneumatics",
            "Motion control (PID, MPC)",
            "Bipedal locomotion",
            "Gait patterns",
        ],
        word_count_target=1050,
        priority="P1",
    ),
    ChapterDefinition(
        number=5,
        title="AI for Robot Control",
        slug="ai-robot-control",
        learning_objectives=[
            "Explain reinforcement learning for robotics",
            "Understand imitation learning approaches",
            "Identify challenges in sim-to-real transfer",
        ],
        topics=[
            "RL (Reinforcement Learning) basics",
            "Policy learning",
            "Sim-to-real gap",
            "Imitation learning",
            "End-to-end learning",
            "Teleoperation",
        ],
        word_count_target=1100,
        priority="P1",
    ),
    ChapterDefinition(
        number=6,
        title="Manipulation and Dexterity",
        slug="manipulation-dexterity",
        learning_objectives=[
            "Describe grasp planning techniques",
            "Explain manipulation primitives",
            "Understand dexterous manipulation challenges",
        ],
        topics=[
            "Grasping",
            "Manipulation planning",
            "Force control",
            "Dexterous hands",
            "Tool use",
            "Object manipulation",
        ],
        word_count_target=1000,
        priority="P1",
    ),
    # Extended Chapters (P2/P3) - Optional, budget permitting
    ChapterDefinition(
        number=7,
        title="Safety and Ethics",
        slug="safety-ethics",
        learning_objectives=[
            "Identify safety considerations in humanoid robotics",
            "Understand ethical implications of embodied AI",
            "Explain regulatory landscape",
        ],
        topics=[
            "Safety standards (ISO)",
            "Human-robot interaction safety",
            "Ethical concerns",
            "Bias in robotics",
            "Regulation",
        ],
        word_count_target=900,
        priority="P3",
    ),
    ChapterDefinition(
        number=8,
        title="Future Trends and Applications",
        slug="future-trends",
        learning_objectives=[
            "Explore emerging applications of humanoid robots",
            "Understand current research frontiers",
            "Envision future developments",
        ],
        topics=[
            "Healthcare robots",
            "Service robots",
            "Space exploration",
            "Research challenges (long-term autonomy, generalization)",
            "Future vision",
        ],
        word_count_target=950,
        priority="P3",
    ),
]


# Curriculum metadata
CURRICULUM_METADATA = {
    "title": "AI-Native Textbook: Physical AI & Humanoid Robotics",
    "description": "An interactive textbook covering fundamentals to advanced topics in Physical AI and humanoid robotics",
    "total_chapters": len(CURRICULUM),
    "mvp_chapters": len([ch for ch in CURRICULUM if ch.priority == "P1"]),
    "extended_chapters": len([ch for ch in CURRICULUM if ch.priority in ["P2", "P3"]]),
    "total_word_count_target": sum(ch.word_count_target for ch in CURRICULUM),
    "estimated_reading_time_minutes": len(CURRICULUM) * 6,  # Average 6 min per chapter
}


def get_curriculum(include_extended: bool = False) -> List[ChapterDefinition]:
    """Get the curriculum for content generation.

    Args:
        include_extended: If True, include P2/P3 chapters (default: False for MVP)

    Returns:
        List of ChapterDefinition objects for generation
    """
    if include_extended:
        return CURRICULUM
    else:
        # MVP: Only P1 chapters (first 6)
        return [ch for ch in CURRICULUM if ch.priority == "P1"]


def get_chapter_by_number(chapter_number: int) -> ChapterDefinition:
    """Get a specific chapter definition by number.

    Args:
        chapter_number: Chapter number (1-8)

    Returns:
        ChapterDefinition for the requested chapter

    Raises:
        ValueError: If chapter_number is invalid
    """
    for chapter in CURRICULUM:
        if chapter.number == chapter_number:
            return chapter
    raise ValueError(f"Invalid chapter number: {chapter_number} (valid: 1-8)")


def get_chapter_by_slug(slug: str) -> ChapterDefinition:
    """Get a specific chapter definition by slug.

    Args:
        slug: URL-friendly slug (e.g., 'physical-ai-intro')

    Returns:
        ChapterDefinition for the requested chapter

    Raises:
        ValueError: If slug is not found
    """
    for chapter in CURRICULUM:
        if chapter.slug == slug:
            return chapter
    raise ValueError(f"Invalid chapter slug: {slug}")


def validate_curriculum() -> List[str]:
    """Validate the curriculum definition.

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Check for duplicate chapter numbers
    numbers = [ch.number for ch in CURRICULUM]
    if len(numbers) != len(set(numbers)):
        errors.append("Duplicate chapter numbers detected")

    # Check for duplicate slugs
    slugs = [ch.slug for ch in CURRICULUM]
    if len(slugs) != len(set(slugs)):
        errors.append("Duplicate chapter slugs detected")

    # Check sequential numbering
    expected_numbers = list(range(1, len(CURRICULUM) + 1))
    if numbers != expected_numbers:
        errors.append(
            f"Chapter numbers not sequential: expected {expected_numbers}, got {numbers}"
        )

    # Check word count targets
    for chapter in CURRICULUM:
        if not (800 <= chapter.word_count_target <= 1200):
            errors.append(
                f"Chapter {chapter.number} word_count_target {chapter.word_count_target} "
                f"outside range (800-1200)"
            )

    # Check learning objectives count (3-5 per chapter)
    for chapter in CURRICULUM:
        obj_count = len(chapter.learning_objectives)
        if not (3 <= obj_count <= 5):
            errors.append(
                f"Chapter {chapter.number} has {obj_count} learning objectives "
                f"(expected 3-5)"
            )

    return errors


# Run validation on import (fail fast if curriculum is invalid)
_validation_errors = validate_curriculum()
if _validation_errors:
    raise ValueError(
        f"Curriculum validation failed:\n" + "\n".join(f"  - {err}" for err in _validation_errors)
    )
