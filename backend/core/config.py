"""
Configuration settings for Nutrition Intelligence Platform
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Optional, Union
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""

    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")

    # API Configuration
    api_title: str = "Nutrition Intelligence API"
    api_version: str = "1.0.0"
    allowed_hosts: Union[str, List[str]] = Field(default="localhost,127.0.0.1")
    cors_origins: Union[str, List[str]] = Field(default="http://localhost:3000,http://localhost:3001")
    
    # Database
    database_url: str = Field(env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Authentication
    secret_key: str = Field(env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=30, env="REFRESH_TOKEN_EXPIRE_DAYS")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    
    # External Services
    google_cloud_storage_bucket: Optional[str] = Field(default=None, env="GCS_BUCKET")
    sendgrid_api_key: Optional[str] = Field(default=None, env="SENDGRID_API_KEY")
    
    # AI Services (Placeholders)
    ai_vision_api_key: Optional[str] = Field(default=None, env="AI_VISION_API_KEY")
    ai_nlp_api_key: Optional[str] = Field(default=None, env="AI_NLP_API_KEY")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # Compliance
    data_retention_days: int = Field(default=2555, env="DATA_RETENTION_DAYS")  # 7 años
    audit_log_enabled: bool = Field(default=True, env="AUDIT_LOG_ENABLED")
    
    # Email
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    otel_exporter_endpoint: Optional[str] = Field(default=None, env="OTEL_EXPORTER_ENDPOINT")
    
    @field_validator("allowed_hosts", "cors_origins", mode="before")
    @classmethod
    def parse_list_from_string(cls, v):
        if isinstance(v, str):
            # Parse comma-separated string into list
            return [item.strip() for item in v.split(",") if item.strip()]
        elif isinstance(v, list):
            # Already a list, just return it
            return v
        # Default fallback
        return []

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()