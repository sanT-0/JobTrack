"""
connection.py — SQLAlchemy engine, session factory, and Base class.

Why: All database setup is in one place. Every part of the application
imports `get_db` (a FastAPI dependency) to get a database session.

How it works:
  - `engine` connects to MySQL (or SQLite for tests).
  - `SessionLocal` is a factory for database sessions.
  - `get_db` yields a session for a single request, then closes it automatically.
  - `Base` is the declarative base all models inherit from.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,      # test connection before use (handles MySQL timeouts)
    pool_recycle=3600,       # recycle connections every hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """All SQLAlchemy models inherit from this Base."""
    pass


def get_db():
    """
    FastAPI dependency that provides a database session per request.

    Usage in route handler:
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
