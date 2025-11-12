"""
Rate Limiting Middleware
========================

Protección contra abuso de API con rate limiting.
"""
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
import time

from core.cache import get_cache


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware de rate limiting usando Redis

    Limita el número de requests por IP/usuario en una ventana de tiempo.
    """

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        exclude_paths: list = None
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/openapi.json"]
        self.cache = get_cache()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Excluir rutas públicas
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Obtener identificador del cliente
        client_id = self._get_client_id(request)

        # Verificar límites
        is_allowed, retry_after = await self._check_rate_limit(client_id)

        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )

        # Procesar request
        response = await call_next(request)

        # Agregar headers de rate limit
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            await self._get_remaining(client_id)
        )

        return response

    def _get_client_id(self, request: Request) -> str:
        """Obtener identificador único del cliente"""
        # Preferir user_id si está autenticado
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"

        # Fallback a IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"

        return f"ip:{ip}"

    async def _check_rate_limit(self, client_id: str) -> tuple[bool, int]:
        """
        Verificar si el cliente ha excedido el límite

        Returns:
            (is_allowed, retry_after_seconds)
        """
        now = int(time.time())

        # Clave para ventana de 1 minuto
        minute_key = f"ratelimit:minute:{client_id}:{now // 60}"
        minute_count = await self.cache.get(minute_key) or 0

        if minute_count >= self.requests_per_minute:
            retry_after = 60 - (now % 60)
            return False, retry_after

        # Clave para ventana de 1 hora
        hour_key = f"ratelimit:hour:{client_id}:{now // 3600}"
        hour_count = await self.cache.get(hour_key) or 0

        if hour_count >= self.requests_per_hour:
            retry_after = 3600 - (now % 3600)
            return False, retry_after

        # Incrementar contadores
        await self.cache.set(minute_key, minute_count + 1, expire=60)
        await self.cache.set(hour_key, hour_count + 1, expire=3600)

        return True, 0

    async def _get_remaining(self, client_id: str) -> int:
        """Obtener requests restantes en la ventana actual"""
        now = int(time.time())
        minute_key = f"ratelimit:minute:{client_id}:{now // 60}"
        minute_count = await self.cache.get(minute_key) or 0
        return max(0, self.requests_per_minute - minute_count)


def rate_limit(requests: int = 10, window: int = 60):
    """
    Decorador para rate limiting en endpoints específicos

    Args:
        requests: Número de requests permitidos
        window: Ventana de tiempo en segundos

    Example:
        @router.get("/expensive-operation")
        @rate_limit(requests=5, window=60)
        async def expensive_operation():
            return {"result": "ok"}
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or args[0]
            cache = get_cache()

            # Obtener identificador del cliente
            user_id = getattr(request.state, "user_id", None)
            client_id = f"user:{user_id}" if user_id else f"ip:{request.client.host}"

            # Verificar rate limit
            now = int(time.time())
            key = f"ratelimit:custom:{func.__name__}:{client_id}:{now // window}"
            count = await cache.get(key) or 0

            if count >= requests:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Max {requests} requests per {window} seconds."
                )

            # Incrementar contador
            await cache.set(key, count + 1, expire=window)

            return await func(*args, **kwargs)

        return wrapper
    return decorator
