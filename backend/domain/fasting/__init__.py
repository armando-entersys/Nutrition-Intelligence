"""
Intermittent Fasting domain models
Based on research 2024-2025 on autophagy and time-restricted eating
"""
from .models import FastingWindow, FastingLog, FastingStats

__all__ = [
    "FastingWindow",
    "FastingLog",
    "FastingStats",
]
