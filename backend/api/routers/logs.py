"""
Frontend Logging Endpoint
Receives and stores logs from the frontend application
"""
from fastapi import APIRouter, Request, HTTPException, status, Depends
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

from core.rate_limit import rate_limit
from core.logging import log_error, log_warning

router = APIRouter()

# ============================================================================
# FRONTEND LOGGER SETUP
# ============================================================================

LOG_DIR = Path("/app/logs") if os.getenv("ENVIRONMENT") == "production" else Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_LOG_FILE = LOG_DIR / "frontend.log"
MAX_BYTES = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5

# Create dedicated frontend logger
frontend_logger = logging.getLogger("frontend")
frontend_logger.setLevel(logging.INFO)
frontend_logger.handlers.clear()

# Rotating file handler
frontend_handler = RotatingFileHandler(
    FRONTEND_LOG_FILE,
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT,
    encoding="utf-8"
)
frontend_handler.setLevel(logging.INFO)

# JSON formatter for frontend logs
class FrontendLogFormatter(logging.Formatter):
    """Custom formatter for frontend logs"""
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "frontend",
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Add extra fields from record
        if hasattr(record, "frontend_data"):
            log_data.update(record.frontend_data)

        return json.dumps(log_data, ensure_ascii=False, default=str)

frontend_handler.setFormatter(FrontendLogFormatter())
frontend_logger.addHandler(frontend_handler)
frontend_logger.propagate = False


# ============================================================================
# SCHEMAS
# ============================================================================

class UserContext(BaseModel):
    """User context from frontend"""
    userId: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class BrowserContext(BaseModel):
    """Browser context from frontend"""
    userAgent: Optional[str] = None
    language: Optional[str] = None
    platform: Optional[str] = None
    screenResolution: Optional[str] = None
    viewport: Optional[str] = None
    url: Optional[str] = None
    referrer: Optional[str] = None


class ErrorContext(BaseModel):
    """Error context"""
    name: Optional[str] = None
    message: Optional[str] = None
    stack: Optional[str] = None


class FrontendLogEntry(BaseModel):
    """Single frontend log entry"""
    timestamp: str
    level: str = Field(..., description="Log level: info, warn, error, debug")
    message: str = Field(..., min_length=1, max_length=1000)
    user: Optional[UserContext] = None
    browser: Optional[BrowserContext] = None
    context: Optional[Dict[str, Any]] = None
    sessionId: Optional[str] = None

    @validator('level')
    def validate_level(cls, v):
        """Validate log level"""
        allowed_levels = ['info', 'warn', 'error', 'debug']
        if v.lower() not in allowed_levels:
            raise ValueError(f'Level must be one of: {", ".join(allowed_levels)}')
        return v.lower()

    @validator('message')
    def validate_message(cls, v):
        """Validate message is not empty"""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class FrontendLogsRequest(BaseModel):
    """Request schema for frontend logs"""
    logs: List[FrontendLogEntry] = Field(..., min_items=1, max_items=50)

    @validator('logs')
    def validate_logs(cls, v):
        """Validate logs list"""
        if not v:
            raise ValueError('Logs list cannot be empty')
        if len(v) > 50:
            raise ValueError('Cannot send more than 50 logs at once')
        return v


class FrontendLogsResponse(BaseModel):
    """Response schema for frontend logs"""
    status: str
    message: str
    logs_received: int
    errors: Optional[List[str]] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/logs/frontend",
    response_model=FrontendLogsResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Receive frontend logs",
    description="Endpoint to receive and store logs from the frontend application"
)
@rate_limit(requests=20, window=60)  # Rate limit: 20 requests per minute
async def receive_frontend_logs(
    request_data: FrontendLogsRequest,
    request: Request
):
    """
    Receive and store logs from frontend application

    Rate limited to prevent abuse: 20 requests per minute

    Args:
        request_data: Frontend logs payload
        request: FastAPI request object

    Returns:
        Response confirming logs received
    """
    errors = []
    logs_processed = 0

    try:
        for log_entry in request_data.logs:
            try:
                # Convert log level to logging level
                level_map = {
                    'info': logging.INFO,
                    'warn': logging.WARNING,
                    'error': logging.ERROR,
                    'debug': logging.DEBUG
                }
                log_level = level_map.get(log_entry.level, logging.INFO)

                # Prepare frontend data
                frontend_data = {
                    "timestamp": log_entry.timestamp,
                    "message": log_entry.message,
                    "level": log_entry.level,
                    "sessionId": log_entry.sessionId,
                }

                # Add user context if available
                if log_entry.user:
                    frontend_data["user"] = log_entry.user.dict(exclude_none=True)

                # Add browser context if available
                if log_entry.browser:
                    frontend_data["browser"] = log_entry.browser.dict(exclude_none=True)

                # Add additional context if available
                if log_entry.context:
                    frontend_data["context"] = log_entry.context

                # Add request metadata
                frontend_data["client_ip"] = request.client.host if request.client else "unknown"
                frontend_data["request_id"] = getattr(request.state, "request_id", None)

                # Log the entry
                frontend_logger.log(
                    log_level,
                    log_entry.message,
                    extra={"frontend_data": frontend_data}
                )

                logs_processed += 1

                # Also log errors to backend error log for visibility
                if log_entry.level == "error":
                    log_warning(
                        f"Frontend Error: {log_entry.message}",
                        business_context={
                            "source": "frontend",
                            "user": log_entry.user.dict(exclude_none=True) if log_entry.user else None,
                            "url": log_entry.browser.url if log_entry.browser else None,
                            "context": log_entry.context
                        }
                    )

            except Exception as e:
                error_msg = f"Error processing log entry: {str(e)}"
                errors.append(error_msg)
                log_error(
                    "Failed to process frontend log entry",
                    error=e,
                    business_context={"log_entry": log_entry.dict()}
                )

        return FrontendLogsResponse(
            status="success" if not errors else "partial_success",
            message=f"Received {logs_processed} logs" + (f" with {len(errors)} errors" if errors else ""),
            logs_received=logs_processed,
            errors=errors if errors else None
        )

    except Exception as e:
        log_error("Error in frontend logs endpoint", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing frontend logs: {str(e)}"
        )


@router.get(
    "/logs/health",
    summary="Frontend logging health check",
    description="Check if frontend logging endpoint is operational"
)
async def frontend_logs_health():
    """
    Health check endpoint for frontend logging

    Returns:
        Status of frontend logging system
    """
    try:
        # Check if log file is writable
        log_file_exists = FRONTEND_LOG_FILE.exists()
        log_dir_writable = os.access(LOG_DIR, os.W_OK)

        return {
            "status": "healthy" if log_dir_writable else "degraded",
            "frontend_log_file": str(FRONTEND_LOG_FILE),
            "log_file_exists": log_file_exists,
            "log_dir_writable": log_dir_writable,
            "max_log_size_mb": MAX_BYTES / (1024 * 1024),
            "backup_count": BACKUP_COUNT
        }
    except Exception as e:
        log_error("Frontend logs health check failed", error=e)
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["router", "frontend_logger"]
