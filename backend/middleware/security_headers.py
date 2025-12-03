"""
Security Headers Middleware for Nutrition Intelligence Platform

Adds security headers to all responses to protect against common web vulnerabilities.
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to all responses.

    Headers added:
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-Frame-Options: Prevents clickjacking
    - X-XSS-Protection: Enables XSS filter in older browsers
    - Referrer-Policy: Controls referrer information
    - Permissions-Policy: Restricts browser features
    - Cache-Control: For sensitive endpoints
    - Strict-Transport-Security: Enforces HTTPS (in production)
    """

    def __init__(self, app, environment: str = "production"):
        super().__init__(app)
        self.environment = environment

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Basic security headers for all responses
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy - restrict dangerous browser features
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )

        # HSTS - Only in production (Cloudflare/Traefik handle SSL)
        if self.environment == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        # Prevent caching of sensitive API responses
        path = request.url.path
        sensitive_paths = ["/api/v1/auth", "/api/v1/users/me", "/health"]
        if any(path.startswith(p) for p in sensitive_paths):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"

        # For documentation endpoints, allow caching but mark as public
        if path in ["/docs", "/redoc", "/openapi.json"]:
            response.headers["Cache-Control"] = "public, max-age=3600"

        return response


class RateLimitByIPMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting by IP for documentation endpoints.
    Prevents abuse of public documentation.

    Note: For production, consider using Redis-based rate limiting
    or Traefik's built-in rate limiting.
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._request_counts: dict = {}
        self._last_cleanup = 0

    async def dispatch(self, request: Request, call_next) -> Response:
        import time

        # Only rate limit documentation endpoints
        path = request.url.path
        if path not in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get client IP (consider X-Forwarded-For for proxied requests)
        client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        if not client_ip:
            client_ip = request.client.host if request.client else "unknown"

        current_time = time.time()
        current_minute = int(current_time / 60)

        # Cleanup old entries every minute
        if current_minute > self._last_cleanup:
            self._request_counts = {
                k: v for k, v in self._request_counts.items()
                if k[1] == current_minute
            }
            self._last_cleanup = current_minute

        # Check rate limit
        key = (client_ip, current_minute)
        count = self._request_counts.get(key, 0)

        if count >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP {client_ip} on {path}")
            return Response(
                content='{"detail": "Rate limit exceeded. Please try again later."}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": "60"}
            )

        self._request_counts[key] = count + 1
        return await call_next(request)
