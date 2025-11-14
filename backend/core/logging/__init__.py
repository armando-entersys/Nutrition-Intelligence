"""
Core Logging Module for Nutrition Intelligence
"""
from .nutrition_logger import (
    nutrition_logger,
    LogLevel,
    log_success,
    log_error,
    log_warning,
    log_info,
    log_nutritional_calculation,
    log_recipe_interaction,
    log_meal_plan_assignment,
    log_equivalences_tracking
)

from .middleware import (
    LoggingMiddleware,
    LoggingContext,
    log_operation
)

# Export logger instance for compatibility
logger = nutrition_logger

__all__ = [
    # Logger principal
    "nutrition_logger",
    "logger",  # Alias for compatibility
    "LogLevel",

    # Funciones de logging directo
    "log_success",
    "log_error",
    "log_warning",
    "log_info",

    # Funciones de negocio específicas
    "log_nutritional_calculation",
    "log_recipe_interaction",
    "log_meal_plan_assignment",
    "log_equivalences_tracking",

    # Middleware y herramientas
    "LoggingMiddleware",
    "LoggingContext",
    "log_operation"
]