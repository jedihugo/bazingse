"""Database connection - Turso (libsql) for production, SQLite for local."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Check for Turso (production) or fall back to local SQLite
TURSO_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if TURSO_URL and TURSO_TOKEN:
    # Production: Use Turso with libsql dialect
    SQLALCHEMY_DATABASE_URL = f"{TURSO_URL}?authToken={TURSO_TOKEN}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # Local development: Use SQLite file
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "bazingse.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from models import Profile  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)
