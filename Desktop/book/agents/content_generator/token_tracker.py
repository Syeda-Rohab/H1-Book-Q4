"""Token usage tracking and cost calculation utility.

Provides centralized token tracking, cost calculation, and analytics
for all LLM generations across the textbook project.

Constitution Compliance: Principle VIII - Observability & Free-Tier Architecture
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


# Anthropic API pricing (as of 2024)
# https://www.anthropic.com/api#pricing
PRICING = {
    "claude-3-haiku-20240307": {
        "input_per_million": 0.25,  # $0.25 per 1M input tokens
        "output_per_million": 1.25,  # $1.25 per 1M output tokens
    },
    "claude-3-sonnet-20240229": {
        "input_per_million": 3.00,  # $3.00 per 1M input tokens
        "output_per_million": 15.00,  # $15.00 per 1M output tokens
    },
}


@dataclass
class TokenUsageRecord:
    """Record of token usage for a single generation.

    Attributes:
        timestamp: ISO 8601 timestamp
        task_type: Type of generation task (chapter/summary/quiz/booster)
        model: Model identifier
        input_tokens: Input tokens consumed
        output_tokens: Output tokens generated
        total_tokens: Total tokens (input + output)
        cost_usd: Estimated cost in USD
        chapter_number: Optional chapter number
        success: Whether generation succeeded
    """

    timestamp: str
    task_type: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    chapter_number: Optional[int] = None
    success: bool = True


class TokenTracker:
    """Centralized token usage tracker for analytics and cost monitoring.

    Features:
    - Records all token usage with timestamps
    - Calculates costs based on Anthropic pricing
    - Generates usage summaries and reports
    - Persists data to JSON file for historical tracking
    - Provides budget warnings

    Usage:
        tracker = TokenTracker()
        tracker.record_usage(
            task_type="chapter",
            model="claude-3-haiku-20240307",
            input_tokens=1000,
            output_tokens=2000,
            chapter_number=1
        )
        summary = tracker.get_summary()
        print(f"Total cost: ${summary['total_cost_usd']:.4f}")
    """

    def __init__(self, data_file: Optional[str] = None):
        """Initialize token tracker.

        Args:
            data_file: Path to JSON file for persisting token data
                      (defaults to .token_usage.json in project root)
        """
        if data_file is None:
            project_root = Path(__file__).parent.parent.parent
            data_file = str(project_root / ".token_usage.json")

        self.data_file = data_file
        self.records: List[TokenUsageRecord] = []
        self._load_records()

        logger.info(f"TokenTracker initialized (data_file={self.data_file})")

    def record_usage(
        self,
        task_type: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        chapter_number: Optional[int] = None,
        success: bool = True,
    ) -> TokenUsageRecord:
        """Record a new token usage event.

        Args:
            task_type: Task type (chapter/summary/quiz/booster)
            model: Model identifier
            input_tokens: Input tokens consumed
            output_tokens: Output tokens generated
            chapter_number: Optional chapter number
            success: Whether generation succeeded

        Returns:
            TokenUsageRecord with calculated cost
        """
        total_tokens = input_tokens + output_tokens
        cost_usd = self._calculate_cost(model, input_tokens, output_tokens)

        record = TokenUsageRecord(
            timestamp=datetime.utcnow().isoformat(),
            task_type=task_type,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
            chapter_number=chapter_number,
            success=success,
        )

        self.records.append(record)
        self._save_records()

        logger.info(
            f"Token usage recorded: {task_type} (tokens={total_tokens}, cost=${cost_usd:.4f})"
        )

        return record

    def get_summary(self) -> Dict:
        """Get summary statistics of all token usage.

        Returns:
            Dictionary with summary statistics including:
            - total_tokens: Total tokens across all records
            - total_cost_usd: Total estimated cost
            - by_task_type: Breakdown by task type
            - by_model: Breakdown by model
            - by_chapter: Breakdown by chapter
            - total_records: Number of records
        """
        if not self.records:
            return {
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "by_task_type": {},
                "by_model": {},
                "by_chapter": {},
                "total_records": 0,
            }

        total_tokens = sum(r.total_tokens for r in self.records)
        total_cost = sum(r.cost_usd for r in self.records)

        # Group by task type
        by_task_type = {}
        for record in self.records:
            if record.task_type not in by_task_type:
                by_task_type[record.task_type] = {
                    "tokens": 0,
                    "cost_usd": 0.0,
                    "count": 0,
                }
            by_task_type[record.task_type]["tokens"] += record.total_tokens
            by_task_type[record.task_type]["cost_usd"] += record.cost_usd
            by_task_type[record.task_type]["count"] += 1

        # Group by model
        by_model = {}
        for record in self.records:
            if record.model not in by_model:
                by_model[record.model] = {"tokens": 0, "cost_usd": 0.0, "count": 0}
            by_model[record.model]["tokens"] += record.total_tokens
            by_model[record.model]["cost_usd"] += record.cost_usd
            by_model[record.model]["count"] += 1

        # Group by chapter
        by_chapter = {}
        for record in self.records:
            if record.chapter_number is not None:
                ch = record.chapter_number
                if ch not in by_chapter:
                    by_chapter[ch] = {"tokens": 0, "cost_usd": 0.0, "count": 0}
                by_chapter[ch]["tokens"] += record.total_tokens
                by_chapter[ch]["cost_usd"] += record.cost_usd
                by_chapter[ch]["count"] += 1

        return {
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost,
            "by_task_type": by_task_type,
            "by_model": by_model,
            "by_chapter": by_chapter,
            "total_records": len(self.records),
        }

    def print_summary(self) -> None:
        """Print a formatted summary of token usage to stdout."""
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print("TOKEN USAGE SUMMARY")
        print("=" * 60)
        print(f"Total Records: {summary['total_records']}")
        print(f"Total Tokens:  {summary['total_tokens']:,}")
        print(f"Total Cost:    ${summary['total_cost_usd']:.4f}")
        print()

        if summary["by_task_type"]:
            print("By Task Type:")
            for task, stats in summary["by_task_type"].items():
                print(
                    f"  {task:12} - {stats['tokens']:>8,} tokens  ${stats['cost_usd']:>7.4f}  ({stats['count']:>2} requests)"
                )
            print()

        if summary["by_model"]:
            print("By Model:")
            for model, stats in summary["by_model"].items():
                model_name = model.split("-")[2] if "-" in model else model
                print(
                    f"  {model_name:12} - {stats['tokens']:>8,} tokens  ${stats['cost_usd']:>7.4f}  ({stats['count']:>2} requests)"
                )
            print()

        if summary["by_chapter"]:
            print("By Chapter:")
            for chapter, stats in sorted(summary["by_chapter"].items()):
                print(
                    f"  Chapter {chapter:2}  - {stats['tokens']:>8,} tokens  ${stats['cost_usd']:>7.4f}  ({stats['count']:>2} requests)"
                )
            print()

        print("=" * 60 + "\n")

    def check_budget(self, budget_usd: float) -> Dict:
        """Check current usage against a budget.

        Args:
            budget_usd: Budget limit in USD

        Returns:
            Dictionary with budget status:
            - budget_usd: Budget limit
            - spent_usd: Amount spent
            - remaining_usd: Remaining budget
            - percent_used: Percentage of budget used
            - over_budget: Whether budget is exceeded
        """
        summary = self.get_summary()
        spent = summary["total_cost_usd"]
        remaining = budget_usd - spent
        percent_used = (spent / budget_usd * 100) if budget_usd > 0 else 0

        return {
            "budget_usd": budget_usd,
            "spent_usd": spent,
            "remaining_usd": remaining,
            "percent_used": percent_used,
            "over_budget": spent > budget_usd,
        }

    def reset(self) -> None:
        """Clear all records (does not delete the data file)."""
        self.records = []
        logger.warning("Token usage records cleared (in-memory)")

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD for token usage.

        Args:
            model: Model identifier
            input_tokens: Input tokens
            output_tokens: Output tokens

        Returns:
            Cost in USD (returns 0.0 if model pricing not found)
        """
        if model not in PRICING:
            logger.warning(f"No pricing found for model: {model}, assuming $0")
            return 0.0

        pricing = PRICING[model]
        input_cost = (input_tokens / 1_000_000) * pricing["input_per_million"]
        output_cost = (output_tokens / 1_000_000) * pricing["output_per_million"]

        return input_cost + output_cost

    def _load_records(self) -> None:
        """Load records from JSON file."""
        if not os.path.exists(self.data_file):
            logger.info(f"Token usage file not found: {self.data_file} (creating new)")
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.records = [TokenUsageRecord(**record) for record in data]
                logger.info(f"Loaded {len(self.records)} token usage records")
        except Exception as e:
            logger.error(f"Failed to load token usage records: {e}")
            self.records = []

    def _save_records(self) -> None:
        """Save records to JSON file."""
        try:
            with open(self.data_file, "w") as f:
                data = [asdict(record) for record in self.records]
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save token usage records: {e}")


# Global tracker instance
_global_tracker: Optional[TokenTracker] = None


def get_global_tracker() -> TokenTracker:
    """Get the global token tracker instance.

    Returns:
        Global TokenTracker instance (creates one if not exists)
    """
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = TokenTracker()
    return _global_tracker


# Convenience function
def record_usage(
    task_type: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    chapter_number: Optional[int] = None,
    success: bool = True,
) -> TokenUsageRecord:
    """Record token usage using the global tracker.

    Args:
        task_type: Task type (chapter/summary/quiz/booster)
        model: Model identifier
        input_tokens: Input tokens consumed
        output_tokens: Output tokens generated
        chapter_number: Optional chapter number
        success: Whether generation succeeded

    Returns:
        TokenUsageRecord with calculated cost
    """
    tracker = get_global_tracker()
    return tracker.record_usage(
        task_type=task_type,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        chapter_number=chapter_number,
        success=success,
    )
