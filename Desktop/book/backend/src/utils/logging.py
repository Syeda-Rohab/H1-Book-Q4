"""Structured logging configuration for observability.

Provides centralized logging setup with structured output, log levels, and
integration with monitoring systems.

Constitution Compliance: Principle VIII - Observability
"""

import os
import sys
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging.

    Outputs logs as JSON for easy parsing by monitoring tools (e.g., ELK, Datadog).

    Attributes:
        environment: Deployment environment (dev/staging/production)
        service_name: Name of the service (for distributed tracing)
    """

    def __init__(
        self,
        environment: str = "development",
        service_name: str = "textbook-backend",
    ):
        """Initialize structured formatter.

        Args:
            environment: Deployment environment
            service_name: Service identifier
        """
        super().__init__()
        self.environment = environment
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON.

        Args:
            record: LogRecord to format

        Returns:
            JSON string representation of log record
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": self.environment,
            "service": self.service_name,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields from log record
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # Add file/line info for debug logs
        if record.levelno == logging.DEBUG:
            log_data["file"] = record.filename
            log_data["line"] = record.lineno
            log_data["function"] = record.funcName

        return json.dumps(log_data)


class SimpleFormatter(logging.Formatter):
    """Simple human-readable formatter for development.

    Outputs logs in a readable format for local development and debugging.
    """

    # Color codes for terminal output
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record for human readability.

        Args:
            record: LogRecord to format

        Returns:
            Formatted log string with colors (if terminal supports it)
        """
        # Color the log level
        level_color = self.COLORS.get(record.levelname, "")
        reset_color = self.COLORS["RESET"]

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        # Build log message
        log_message = (
            f"{timestamp} | "
            f"{level_color}{record.levelname:8}{reset_color} | "
            f"{record.name:25} | "
            f"{record.getMessage()}"
        )

        # Add exception info if present
        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"

        return log_message


def setup_logging(
    level: Optional[str] = None,
    structured: Optional[bool] = None,
    log_file: Optional[str] = None,
) -> None:
    """Configure structured logging for the application.

    Args:
        level: Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
               Defaults to LOG_LEVEL env var or INFO
        structured: Use structured JSON logging (True) or simple formatting (False)
                   Defaults to STRUCTURED_LOGGING env var or False for development
        log_file: Optional file path for log output (in addition to stdout)
                 Defaults to LOG_FILE env var

    Usage:
        # Development
        setup_logging(level="DEBUG", structured=False)

        # Production
        setup_logging(level="INFO", structured=True, log_file="/var/log/app.log")
    """
    # Get configuration from environment or parameters
    log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()
    use_structured = (
        structured
        if structured is not None
        else os.getenv("STRUCTURED_LOGGING", "false").lower() == "true"
    )
    log_file_path = log_file or os.getenv("LOG_FILE")
    environment = os.getenv("ENVIRONMENT", "development")
    service_name = os.getenv("SERVICE_NAME", "textbook-backend")

    # Validate log level
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        print(f"Invalid log level: {log_level}, defaulting to INFO", file=sys.stderr)
        numeric_level = logging.INFO

    # Create formatter
    if use_structured:
        formatter = StructuredFormatter(
            environment=environment, service_name=service_name
        )
    else:
        formatter = SimpleFormatter()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(numeric_level)
    stdout_handler.setFormatter(formatter)
    root_logger.addHandler(stdout_handler)

    # Add file handler if specified
    if log_file_path:
        try:
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to setup file logging: {e}", file=sys.stderr)

    # Log initial message
    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging configured (level={log_level}, structured={use_structured}, "
        f"environment={environment})"
    )

    # Adjust log levels for noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str, extra_fields: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """Get a logger with optional extra fields.

    Args:
        name: Logger name (typically __name__)
        extra_fields: Optional dictionary of extra fields to include in all logs

    Returns:
        Logger instance with configured formatting

    Usage:
        logger = get_logger(__name__, extra_fields={"component": "chapter_generator"})
        logger.info("Chapter generated successfully")
    """
    logger = logging.getLogger(name)

    # Add extra fields as adapter if provided
    if extra_fields:
        logger = LoggerAdapter(logger, extra_fields)

    return logger


class LoggerAdapter(logging.LoggerAdapter):
    """Adapter to add extra fields to all log records.

    Attributes:
        extra_fields: Dictionary of fields to add to each log record
    """

    def __init__(self, logger: logging.Logger, extra_fields: Dict[str, Any]):
        """Initialize logger adapter.

        Args:
            logger: Base logger instance
            extra_fields: Fields to add to each log record
        """
        super().__init__(logger, {})
        self.extra_fields = extra_fields

    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Process log message and add extra fields.

        Args:
            msg: Log message
            kwargs: Log kwargs

        Returns:
            Tuple of (message, kwargs) with extra fields added
        """
        # Add extra fields to the log record
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"]["extra_fields"] = self.extra_fields

        return msg, kwargs


# Convenience functions for common log patterns

def log_api_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
) -> None:
    """Log an API request with structured fields.

    Args:
        logger: Logger instance
        method: HTTP method (GET/POST/etc.)
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
    """
    logger.info(
        f"{method} {path} - {status_code} ({duration_ms:.2f}ms)",
        extra={
            "extra_fields": {
                "http_method": method,
                "http_path": path,
                "http_status": status_code,
                "duration_ms": duration_ms,
            }
        },
    )


def log_llm_generation(
    logger: logging.Logger,
    task: str,
    model: str,
    tokens_used: int,
    duration_ms: float,
    success: bool,
) -> None:
    """Log an LLM generation request with structured fields.

    Args:
        logger: Logger instance
        task: Task type (chapter/summary/quiz/booster)
        model: Model identifier
        tokens_used: Tokens consumed
        duration_ms: Generation duration in milliseconds
        success: Whether generation succeeded
    """
    status = "success" if success else "failed"
    logger.info(
        f"LLM generation {status} (task={task}, tokens={tokens_used}, {duration_ms:.2f}ms)",
        extra={
            "extra_fields": {
                "llm_task": task,
                "llm_model": model,
                "llm_tokens": tokens_used,
                "duration_ms": duration_ms,
                "success": success,
            }
        },
    )


def log_validation(
    logger: logging.Logger,
    content_type: str,
    valid: bool,
    errors: Optional[list] = None,
) -> None:
    """Log content validation with structured fields.

    Args:
        logger: Logger instance
        content_type: Type of content validated
        valid: Whether validation passed
        errors: Optional list of validation errors
    """
    if valid:
        logger.info(
            f"{content_type} validation passed",
            extra={"extra_fields": {"content_type": content_type, "valid": True}},
        )
    else:
        logger.warning(
            f"{content_type} validation failed ({len(errors or [])} errors)",
            extra={
                "extra_fields": {
                    "content_type": content_type,
                    "valid": False,
                    "errors": errors or [],
                }
            },
        )
