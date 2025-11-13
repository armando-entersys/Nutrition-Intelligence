"""
Sentry Error Monitoring Configuration
======================================

Configures Sentry for error tracking and performance monitoring.
"""
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
from core.config import get_settings

settings = get_settings()


def init_sentry():
    """
    Initialize Sentry SDK with FastAPI, SQLAlchemy, and Redis integrations.

    Features:
    - Error tracking with full stack traces
    - Performance monitoring (transactions)
    - Release tracking
    - Environment-specific configuration
    - User context tracking
    - Breadcrumbs for debugging
    """
    if not settings.sentry_dsn:
        logging.warning("Sentry DSN not configured. Error monitoring disabled.")
        return

    # Configure logging integration
    logging_integration = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,

        # Integrations
        integrations=[
            FastApiIntegration(
                transaction_style="endpoint",  # Use endpoint name as transaction
            ),
            SqlalchemyIntegration(),
            RedisIntegration(),
            logging_integration,
        ],

        # Performance Monitoring
        traces_sample_rate=1.0 if settings.environment == "development" else 0.1,

        # Error Sampling
        sample_rate=1.0,  # Capture 100% of errors

        # Release tracking
        release=f"nutrition-intelligence@{settings.api_version}",

        # Additional options
        send_default_pii=False,  # Don't send personally identifiable information
        attach_stacktrace=True,   # Attach stack trace to all messages
        max_breadcrumbs=50,       # Keep last 50 breadcrumbs

        # Before send hook to filter sensitive data
        before_send=before_send_hook,
    )

    logging.info(f"Sentry initialized for environment: {settings.environment}")


def before_send_hook(event, hint):
    """
    Filter sensitive data before sending to Sentry.

    Args:
        event: The event dictionary
        hint: Additional information about the event

    Returns:
        Modified event or None to drop the event
    """
    # Filter out sensitive headers
    if "request" in event:
        headers = event["request"].get("headers", {})
        sensitive_headers = ["authorization", "cookie", "x-api-key"]

        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[Filtered]"

    # Filter out sensitive query parameters
    if "request" in event and "query_string" in event["request"]:
        query = event["request"]["query_string"]
        if "password" in query or "token" in query:
            event["request"]["query_string"] = "[Filtered]"

    # Don't send health check errors
    if "request" in event:
        url = event["request"].get("url", "")
        if "/health" in url or "/metrics" in url:
            return None

    return event


def capture_exception(error: Exception, context: dict = None):
    """
    Manually capture an exception with additional context.

    Args:
        error: The exception to capture
        context: Additional context dictionary
    """
    if context:
        with sentry_sdk.configure_scope() as scope:
            for key, value in context.items():
                scope.set_context(key, value)

    sentry_sdk.capture_exception(error)


def capture_message(message: str, level: str = "info", context: dict = None):
    """
    Capture a message in Sentry.

    Args:
        message: The message to capture
        level: Message level (info, warning, error)
        context: Additional context dictionary
    """
    if context:
        with sentry_sdk.configure_scope() as scope:
            for key, value in context.items():
                scope.set_context(key, value)

    sentry_sdk.capture_message(message, level=level)


def set_user_context(user_id: int, email: str = None, role: str = None):
    """
    Set user context for Sentry events.

    Args:
        user_id: User ID
        email: User email (optional)
        role: User role (optional)
    """
    with sentry_sdk.configure_scope() as scope:
        scope.set_user({
            "id": str(user_id),
            "email": email,
            "role": role,
        })


def add_breadcrumb(message: str, category: str, level: str = "info", data: dict = None):
    """
    Add a breadcrumb for debugging.

    Args:
        message: Breadcrumb message
        category: Category (e.g., "auth", "database", "api")
        level: Level (debug, info, warning, error)
        data: Additional data
    """
    sentry_sdk.add_breadcrumb(
        message=message,
        category=category,
        level=level,
        data=data or {}
    )


def start_transaction(name: str, op: str = "function"):
    """
    Start a performance monitoring transaction.

    Args:
        name: Transaction name
        op: Operation type (function, http.request, db.query, etc.)

    Returns:
        Transaction context manager
    """
    return sentry_sdk.start_transaction(name=name, op=op)
