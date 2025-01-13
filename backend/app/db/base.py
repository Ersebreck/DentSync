"""
Database configuration and session management.
This module sets up the SQLAlchemy engine and session factory for database operations.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.settings import settings

# Create database engine using settings
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True  # Enables connection pool "pre-ping" feature
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()