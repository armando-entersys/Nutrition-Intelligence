"""
Redis Cache Configuration
=========================

Configuración de caché con Redis para optimizar rendimiento.
"""
import json
import pickle
from typing import Any, Optional, Union
from functools import wraps
import hashlib

import redis.asyncio as aioredis
from core.config import get_settings


class CacheManager:
    """
    Gestor de caché con Redis

    Proporciona funciones para cachear datos y reducir carga en la base de datos.
    """

    def __init__(self):
        self.settings = get_settings()
        self._redis = None

    async def get_redis(self) -> aioredis.Redis:
        """Obtener conexión a Redis"""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self.settings.redis_url,
                encoding="utf-8",
                decode_responses=False
            )
        return self._redis

    async def get(self, key: str) -> Optional[Any]:
        """
        Obtener valor del caché

        Args:
            key: Clave del caché

        Returns:
            Valor deserializado o None si no existe
        """
        redis = await self.get_redis()
        value = await redis.get(key)

        if value is None:
            return None

        try:
            # Intentar deserializar con pickle primero (más rápido)
            return pickle.loads(value)
        except:
            # Fallback a JSON
            return json.loads(value.decode('utf-8'))

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 300  # 5 minutos por defecto
    ) -> bool:
        """
        Guardar valor en caché

        Args:
            key: Clave del caché
            value: Valor a guardar
            expire: Tiempo de expiración en segundos

        Returns:
            True si se guardó correctamente
        """
        redis = await self.get_redis()

        try:
            # Serializar con pickle (más rápido y soporta más tipos)
            serialized = pickle.dumps(value)
        except:
            # Fallback a JSON
            serialized = json.dumps(value).encode('utf-8')

        return await redis.setex(key, expire, serialized)

    async def delete(self, key: str) -> bool:
        """Eliminar clave del caché"""
        redis = await self.get_redis()
        return await redis.delete(key) > 0

    async def clear_pattern(self, pattern: str) -> int:
        """
        Eliminar todas las claves que coincidan con un patrón

        Args:
            pattern: Patrón de búsqueda (e.g., "user:*")

        Returns:
            Número de claves eliminadas
        """
        redis = await self.get_redis()
        keys = await redis.keys(pattern)
        if keys:
            return await redis.delete(*keys)
        return 0

    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generar clave de caché única basada en argumentos

        Args:
            prefix: Prefijo de la clave
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados

        Returns:
            Clave única para caché
        """
        # Crear hash de los argumentos
        key_data = f"{args}:{sorted(kwargs.items())}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()[:8]
        return f"{prefix}:{key_hash}"


# Singleton global
_cache_manager = None


def get_cache() -> CacheManager:
    """Obtener instancia global del cache manager"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cached(
    prefix: str,
    expire: int = 300,
    key_builder: Optional[callable] = None
):
    """
    Decorador para cachear resultados de funciones async

    Args:
        prefix: Prefijo para la clave de caché
        expire: Tiempo de expiración en segundos
        key_builder: Función personalizada para construir la clave

    Example:
        @cached(prefix="user", expire=600)
        async def get_user(user_id: int):
            return await db.get(User, user_id)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = get_cache()

            # Construir clave de caché
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                cache_key = cache.cache_key(prefix, *args, **kwargs)

            # Intentar obtener del caché
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Ejecutar función y cachear resultado
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, expire)

            return result

        return wrapper
    return decorator


# Configuración de tiempos de expiración por tipo de dato
CACHE_EXPIRATION = {
    "user": 600,           # 10 minutos
    "product": 1800,       # 30 minutos
    "food": 1800,          # 30 minutos
    "rag_search": 300,     # 5 minutos
    "nutritionist": 900,   # 15 minutos
    "patient": 300,        # 5 minutos
    "recipe": 1800,        # 30 minutos
    "meal_plan": 600,      # 10 minutos
}
