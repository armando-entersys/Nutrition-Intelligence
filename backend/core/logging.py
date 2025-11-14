"""
Comprehensive Logging System for Nutrition Intelligence Platform
Provides structured logging with rotation, JSON formatting, and middleware
"""
import logging
import json
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import traceback


# ============================================================================
# CONFIGURATION
# ============================================================================

LOG_DIR = Path("/app/logs") if os.getenv("ENVIRONMENT") == "production" else Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

APP_LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"
ACCESS_LOG_FILE = LOG_DIR / "access.log"

MAX_BYTES = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
JSON_LOG_FORMAT = True  # Enable JSON structured logging


# ============================================================================
# CUSTOM JSON FORMATTER
# ============================================================================

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    """
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        if hasattr(record, "business_context"):
            log_data["business_context"] = record.business_context

        if hasattr(record, "endpoint"):
            log_data["endpoint"] = record.endpoint

        if hasattr(record, "method"):
            log_data["method"] = record.method

        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code

        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }

        return json.dumps(log_data, ensure_ascii=False, default=str)


# ============================================================================
# LOGGER SETUP
# ============================================================================

def setup_logger(
    name: str = "nutrition_intelligence",
    level: int = logging.INFO,
    use_json: bool = True
) -> logging.Logger:
    """
    Setup and configure logger with rotating file handlers and console output

    Args:
        name: Logger name
        level: Logging level
        use_json: Whether to use JSON formatting

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Choose formatter
    if use_json:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(LOG_FORMAT)

    # Console Handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    if use_json:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))
    logger.addHandler(console_handler)

    # Rotating File Handler for general app logs
    app_file_handler = RotatingFileHandler(
        APP_LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(formatter)
    logger.addHandler(app_file_handler)

    # Rotating File Handler for errors only
    error_file_handler = RotatingFileHandler(
        ERROR_LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    # Rotating File Handler for access logs
    access_file_handler = RotatingFileHandler(
        ACCESS_LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    access_file_handler.setLevel(logging.INFO)
    access_file_handler.setFormatter(formatter)

    # Create separate logger for access logs
    access_logger = logging.getLogger(f"{name}.access")
    access_logger.setLevel(logging.INFO)
    access_logger.handlers.clear()
    access_logger.addHandler(access_file_handler)
    access_logger.propagate = False

    return logger


# Initialize default logger
logger = setup_logger()


# ============================================================================
# CONVENIENCE LOGGING FUNCTIONS
# ============================================================================

def log_info(
    message: str,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    business_context: Optional[Dict[str, Any]] = None,
    **kwargs
):
    """
    Log info level message with optional context

    Args:
        message: Log message
        request_id: Optional request ID
        user_id: Optional user ID
        business_context: Optional business context data
        **kwargs: Additional context
    """
    extra = {
        "request_id": request_id,
        "user_id": user_id,
        "business_context": business_context,
        **kwargs
    }
    logger.info(message, extra={k: v for k, v in extra.items() if v is not None})


def log_success(
    message: str,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    business_context: Optional[Dict[str, Any]] = None,
    **kwargs
):
    """
    Log successful operation (info level with success flag)

    Args:
        message: Log message
        request_id: Optional request ID
        user_id: Optional user ID
        business_context: Optional business context data
        **kwargs: Additional context
    """
    extra = {
        "request_id": request_id,
        "user_id": user_id,
        "business_context": {**(business_context or {}), "success": True},
        **kwargs
    }
    logger.info(f"✓ {message}", extra={k: v for k, v in extra.items() if v is not None})


def log_warning(
    message: str,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    business_context: Optional[Dict[str, Any]] = None,
    **kwargs
):
    """
    Log warning level message with optional context

    Args:
        message: Log message
        request_id: Optional request ID
        user_id: Optional user ID
        business_context: Optional business context data
        **kwargs: Additional context
    """
    extra = {
        "request_id": request_id,
        "user_id": user_id,
        "business_context": business_context,
        **kwargs
    }
    logger.warning(message, extra={k: v for k, v in extra.items() if v is not None})


def log_error(
    message: str,
    error: Optional[Exception] = None,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    business_context: Optional[Dict[str, Any]] = None,
    **kwargs
):
    """
    Log error level message with optional exception and context

    Args:
        message: Log message
        error: Optional exception object
        request_id: Optional request ID
        user_id: Optional user ID
        business_context: Optional business context data
        **kwargs: Additional context
    """
    extra = {
        "request_id": request_id,
        "user_id": user_id,
        "business_context": business_context,
        **kwargs
    }

    if error:
        logger.error(
            f"{message}: {str(error)}",
            exc_info=error,
            extra={k: v for k, v in extra.items() if v is not None}
        )
    else:
        logger.error(
            message,
            extra={k: v for k, v in extra.items() if v is not None}
        )


# ============================================================================
# FASTAPI LOGGING MIDDLEWARE
# ============================================================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for request/response logging
    Logs all HTTP requests with timing, status codes, and context
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.access_logger = logging.getLogger("nutrition_intelligence.access")

    async def dispatch(self, request: Request, call_next):
        """
        Process request and log details

        Args:
            request: FastAPI request object
            call_next: Next middleware in chain

        Returns:
            Response object
        """
        # Generate request ID if not present
        request_id = getattr(request.state, "request_id", None)
        if not request_id:
            import uuid
            request_id = str(uuid.uuid4())
            request.state.request_id = request_id

        # Extract request details
        method = request.method
        url = str(request.url)
        endpoint = request.url.path
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        # Start timer
        start_time = time.time()

        # Process request
        try:
            response = await call_next(request)
            status_code = response.status_code
            error = None
        except Exception as e:
            status_code = 500
            error = e
            raise
        finally:
            # Calculate duration
            duration_ms = round((time.time() - start_time) * 1000, 2)

            # Extract user info if available
            user_id = None
            if hasattr(request.state, "user"):
                user_id = getattr(request.state.user, "id", None)

            # Log access
            log_level = logging.INFO if status_code < 400 else logging.ERROR

            self.access_logger.log(
                log_level,
                f"{method} {endpoint} - {status_code}",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "endpoint": endpoint,
                    "url": url,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "client_host": client_host,
                    "user_agent": user_agent,
                    "user_id": user_id,
                }
            )

        return response


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "setup_logger",
    "logger",
    "log_info",
    "log_success",
    "log_warning",
    "log_error",
    "LoggingMiddleware",
    "JSONFormatter",
]
