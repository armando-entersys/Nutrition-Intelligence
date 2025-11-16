"""
Global Error Handler Middleware
================================

Catches and handles all unhandled exceptions in the application.
Integrates with Sentry for error tracking.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from core.sentry import capture_exception, add_breadcrumb

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions (4xx, 5xx errors).

    Args:
        request: The request object
        exc: The HTTP exception

    Returns:
        JSON response with error details
    """
    # Add breadcrumb for debugging
    add_breadcrumb(
        message=f"HTTP {exc.status_code}: {exc.detail}",
        category="http.error",
        level="warning" if exc.status_code < 500 else "error",
        data={
            "url": str(request.url),
            "method": request.method,
            "status_code": exc.status_code,
        }
    )

    # Only log server errors
    if exc.status_code >= 500:
        logger.error(
            f"HTTP {exc.status_code} error: {exc.detail}",
            extra={
                "url": str(request.url),
                "method": request.method,
            }
        )
        # Capture in Sentry
        capture_exception(exc, context={
            "http": {
                "url": str(request.url),
                "method": request.method,
                "status_code": exc.status_code,
            }
        })

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_error"
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors (422).

    Args:
        request: The request object
        exc: The validation error

    Returns:
        JSON response with validation error details
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    # Add breadcrumb
    add_breadcrumb(
        message="Request validation failed",
        category="validation.error",
        level="warning",
        data={
            "url": str(request.url),
            "method": request.method,
            "errors": errors,
        }
    )

    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {errors}",
        extra={"errors": errors}
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Validation error",
                "type": "validation_error",
                "details": errors
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all unhandled exceptions.

    Args:
        request: The request object
        exc: The exception

    Returns:
        JSON response with error details
    """
    # Add breadcrumb
    add_breadcrumb(
        message=f"Unhandled exception: {type(exc).__name__}",
        category="exception",
        level="error",
        data={
            "url": str(request.url),
            "method": request.method,
            "exception_type": type(exc).__name__,
        }
    )

    # Log the error
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True,
        extra={
            "url": str(request.url),
            "method": request.method,
        }
    )

    # Capture in Sentry
    capture_exception(exc, context={
        "http": {
            "url": str(request.url),
            "method": request.method,
        }
    })

    # Return generic error response (don't expose internal details)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal server error",
                "type": "internal_error"
            }
        }
    )
