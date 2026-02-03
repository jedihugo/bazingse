"""SQLite database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database file path - use Railway volume, /tmp, or local
if os.environ.get("RAILWAY_ENVIRONMENT"):
    # Railway: use /tmp for now (add volume for persistence later)
    DATABASE_PATH = "/tmp/bazingse.db"
else:
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "bazingse.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
print(f"Using database: {DATABASE_PATH}")

# Create engine with check_same_thread=False for SQLite
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
