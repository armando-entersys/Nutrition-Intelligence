"""
Database configuration and session management
"""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from core.config import get_settings

logger = logging.getLogger(__name__)

# Database engines
engine = None
async_engine = None
SessionLocal = None
AsyncSessionLocal = None

def init_database():
    """Initialize database engines and session factories"""
    global engine, async_engine, SessionLocal, AsyncSessionLocal
    
    settings = get_settings()

    # Sync engine - force psycopg2 driver
    sync_database_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    # Use default postgresql:// which uses psycopg2 when available
    if "postgresql://" not in sync_database_url:
        sync_database_url = sync_database_url.replace("postgresql+psycopg2://", "postgresql://")

    engine = create_engine(
        sync_database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
        pool_recycle=300
    )

    # Async engine for API operations
    async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    if "postgresql+asyncpg://" not in async_database_url:
        async_database_url = async_database_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    async_engine = create_async_engine(
        async_database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
        pool_recycle=300
    )
    
    # Session factories
    SessionLocal = sessionmaker(engine, class_=Session, expire_on_commit=False)
    AsyncSessionLocal = sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    logger.info("Database engines initialized")

async def init_db():
    """Initialize database connection"""
    init_database()

    # Tables are created via SQL scripts (backend/scripts/init_tables.sql)
    # Not using SQLModel.metadata.create_all to avoid duplicate index issues
    logger.info("Database initialized")

def get_session() -> Session:
    """Get synchronous database session"""
    if not SessionLocal:
        init_database()
    
    with SessionLocal() as session:
        yield session

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get asynchronous database session"""
    if not AsyncSessionLocal:
        init_database()
    
    async with AsyncSessionLocal() as session:
        yield session

get_db = get_async_session

@asynccontextmanager
async def get_db_transaction():
    """Get database session with transaction management"""
    if not AsyncSessionLocal:
        init_database()
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()