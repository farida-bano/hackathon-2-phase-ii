"""
Database connection and session management with production settings.
"""

import logging
from sqlmodel import Session, create_engine

from src.config import settings

logger = logging.getLogger(__name__)

# Connection pool settings based on environment
if settings.is_production:
    # Production: Use pooling with Railway/Neon
    engine = create_engine(
        settings.neon_database_url,
        echo=False,
        # Pool configuration for production
        pool_size=10,  # Base pool size
        max_overflow=20,  # Additional connections when needed
        pool_pre_ping=True,  # Verify connections are alive
        pool_recycle=3600,  # Recycle connections every hour
        connect_args={
            "connect_timeout": 10,
            "application_name": "todo_app_prod",
            "options": "-c statement_timeout=30000",  # 30s statement timeout
        },
    )
else:
    # Development: Simpler configuration
    engine = create_engine(
        settings.neon_database_url,
        echo=True,  # SQL logging in development
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def get_session():
    """
    Dependency function to get database session.
    Uses connection pooling automatically.
    """
    with Session(engine) as session:
        yield session
