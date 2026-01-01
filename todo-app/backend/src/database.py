"""
Database connection and session management.
"""

from sqlmodel import Session, create_engine

from src.config import settings

# Create database engine with connection pooling
engine = create_engine(
    settings.neon_database_url,
    echo=False,  # Set to True for SQL query logging during development
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Maximum overflow connections
)


def get_session():
    """
    Dependency function to get database session.
    Yields a session and ensures it's closed after use.
    """
    with Session(engine) as session:
        yield session
