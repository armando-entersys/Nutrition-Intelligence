"""
Simple configuration for testing
"""
import os

class SimpleSettings:
    def __init__(self):
        self.environment = "development"
        self.debug = True
        self.database_url = "postgresql://postgres:postgres@postgres:5432/nutrition_intelligence"
        self.redis_url = "redis://redis:6379/0"
        self.secret_key = "your-super-secret-key-change-in-production-minimum-32-chars-long"
        self.allowed_hosts = ["*"]
        self.cors_origins = ["*"]
        self.access_token_expire_minutes = 30
        self.algorithm = "HS256"

def get_simple_settings():
    return SimpleSettings()