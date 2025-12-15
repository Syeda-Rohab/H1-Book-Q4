"""Utility modules for backend services.

This package contains shared utility functions and configurations:
- Logging configuration
- Helper functions
"""

from .logging import setup_logging, get_logger

__all__ = ["setup_logging", "get_logger"]
