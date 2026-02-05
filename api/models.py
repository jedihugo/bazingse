"""SQLAlchemy ORM models for BaZi application.

Includes:
- Profile: Birth data storage
- LifeEvent: Normalized life events with pattern correlations
- BaZiPattern: Pattern definitions with validation statistics
- EventPatternLink: Many-to-many linking events to patterns
- PatternStatistics: Accuracy tracking per pattern per domain
"""

from sqlalchemy import (
    Column, String, DateTime, JSON, Float, Integer, Boolean,
    ForeignKey, Text, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


# =============================================================================
# ENUMS
# =============================================================================

class ValidationStatus(enum.Enum):
    """Status of pattern-event link validation."""
    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"
    UNCERTAIN = "uncertain"


class EventSentiment(enum.Enum):
    """Event sentiment classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class EventSeverity(enum.Enum):
    """Event severity levels."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


# =============================================================================
# PROFILE MODEL (Existing)
# =============================================================================

class Profile(Base):
    """Profile model for storing birth data."""

    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)  # YYYY-MM-DD format
    birth_time = Column(String, nullable=True)   # HH:MM format or NULL for unknown
    gender = Column(String, nullable=False)      # "male" or "female"
    place_of_birth = Column(String, nullable=True)  # City/location string
    phone = Column(String, nullable=True, unique=True)  # Mobile/WhatsApp number (unique identifier)
    life_events = Column(JSON, nullable=True, default=list)  # Legacy: Array of life event objects
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    events = relationship("LifeEvent", back_populates="profile", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "birth_time": self.birth_time,
            "gender": self.gender,
            "place_of_birth": self.place_of_birth,
            "phone": self.phone,
            "life_events": self.life_events or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# =============================================================================
# LIFE EVENT MODEL
# =============================================================================

class LifeEvent(Base):
    """
    Normalized life event storage.

    Each event has:
    - Profile association (whose life event)
    - Date and type classification
    - Pattern correlations through EventPatternLink
    """

    __tablename__ = "life_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)

    # Event details
    event_date = Column(String, nullable=False)  # YYYY-MM-DD
    event_time = Column(String, nullable=True)   # HH:MM or NULL
    life_domain = Column(String, nullable=False)  # health, wealth, career, etc.
    event_type = Column(String, nullable=False)   # illness_major, promotion, etc.
    event_title = Column(String, nullable=True)   # User-provided title
    event_description = Column(Text, nullable=True)  # Detailed description

    # Classification
    sentiment = Column(SQLEnum(EventSentiment), nullable=True)
    severity = Column(SQLEnum(EventSeverity), nullable=True)

    # Analysis metadata
    analysis_snapshot = Column(JSON, nullable=True)  # BaZi chart state at event time
    auto_detected_patterns = Column(JSON, nullable=True)  # System-detected patterns

    # User validation
    user_validated = Column(Boolean, default=False)
    user_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="events")
    pattern_links = relationship("EventPatternLink", back_populates="event", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "life_domain": self.life_domain,
            "event_type": self.event_type,
            "event_title": self.event_title,
            "event_description": self.event_description,
            "sentiment": self.sentiment.value if self.sentiment else None,
            "severity": self.severity.value if self.severity else None,
            "user_validated": self.user_validated,
            "user_notes": self.user_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# =============================================================================
# BAZI PATTERN MODEL
# =============================================================================

class BaZiPattern(Base):
    """
    Pattern definition storage.

    Stores pattern metadata and aggregate statistics.
    Links to specific PatternSpec definitions in code.
    """

    __tablename__ = "bazi_patterns"

    id = Column(String, primary_key=True)  # Pattern ID from PatternSpec (e.g., "PUNISHMENT~Yin-Si-Shen~shi_xing")
    category = Column(String, nullable=False)  # punishment, clash, six_harmonies, etc.
    chinese_name = Column(String, nullable=True)
    english_name = Column(String, nullable=True)

    # Pattern details
    participants = Column(JSON, nullable=True)  # List of stems/branches
    resulting_element = Column(String, nullable=True)  # For transformations
    is_positive = Column(Boolean, default=True)  # Positive or negative pattern

    # Scoring metadata
    base_score = Column(Float, default=10.0)
    default_sentiment = Column(SQLEnum(EventSentiment), nullable=True)

    # Aggregate statistics (updated by triggers/cron)
    total_event_links = Column(Integer, default=0)
    validated_links = Column(Integer, default=0)
    rejected_links = Column(Integer, default=0)
    precision_score = Column(Float, nullable=True)  # validated / (validated + rejected)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    event_links = relationship("EventPatternLink", back_populates="pattern")
    statistics = relationship("PatternStatistics", back_populates="pattern", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "category": self.category,
            "chinese_name": self.chinese_name,
            "english_name": self.english_name,
            "participants": self.participants,
            "resulting_element": self.resulting_element,
            "is_positive": self.is_positive,
            "base_score": self.base_score,
            "total_event_links": self.total_event_links,
            "validated_links": self.validated_links,
            "rejected_links": self.rejected_links,
            "precision_score": self.precision_score,
        }


# =============================================================================
# EVENT-PATTERN LINK MODEL
# =============================================================================

class EventPatternLink(Base):
    """
    Many-to-many relationship between life events and BaZi patterns.

    Each link represents a hypothesis: "This pattern contributed to this event."
    Validation status indicates whether user confirmed the correlation.
    """

    __tablename__ = "event_pattern_links"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String, ForeignKey("life_events.id"), nullable=False)
    pattern_id = Column(String, ForeignKey("bazi_patterns.id"), nullable=False)

    # Link metadata
    contribution_weight = Column(Float, default=1.0)  # How much this pattern contributed
    calculated_severity = Column(Float, nullable=True)  # System-calculated severity
    distance = Column(Integer, nullable=True)  # Distance between pattern nodes

    # Validation
    validation_status = Column(SQLEnum(ValidationStatus), default=ValidationStatus.PENDING)
    system_confidence = Column(Float, default=0.5)  # 0-1 confidence score
    user_rating = Column(Integer, nullable=True)  # 1-5 user accuracy rating
    validation_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    validated_at = Column(DateTime, nullable=True)

    # Relationships
    event = relationship("LifeEvent", back_populates="pattern_links")
    pattern = relationship("BaZiPattern", back_populates="event_links")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "event_id": self.event_id,
            "pattern_id": self.pattern_id,
            "contribution_weight": self.contribution_weight,
            "calculated_severity": self.calculated_severity,
            "distance": self.distance,
            "validation_status": self.validation_status.value if self.validation_status else None,
            "system_confidence": self.system_confidence,
            "user_rating": self.user_rating,
            "validation_notes": self.validation_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "validated_at": self.validated_at.isoformat() if self.validated_at else None,
        }


# =============================================================================
# PATTERN STATISTICS MODEL
# =============================================================================

class PatternStatistics(Base):
    """
    Domain-specific accuracy statistics for each pattern.

    Tracks precision, recall, and F1 score per pattern per life domain.
    Updated automatically when EventPatternLinks are validated.
    """

    __tablename__ = "pattern_statistics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pattern_id = Column(String, ForeignKey("bazi_patterns.id"), nullable=False)
    life_domain = Column(String, nullable=False)  # health, wealth, career, etc.

    # Core metrics
    true_positives = Column(Integer, default=0)   # Validated links
    false_positives = Column(Integer, default=0)  # Rejected links
    total_predictions = Column(Integer, default=0)  # All links for this domain

    # Calculated scores
    precision_score = Column(Float, nullable=True)  # TP / (TP + FP)
    recall_score = Column(Float, nullable=True)     # TP / (TP + FN) - requires ground truth
    f1_score = Column(Float, nullable=True)         # 2 * (P * R) / (P + R)

    # Confidence
    sample_size_confidence = Column(Float, default=0.0)  # Higher with more samples
    last_calculated = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    pattern = relationship("BaZiPattern", back_populates="statistics")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "pattern_id": self.pattern_id,
            "life_domain": self.life_domain,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "total_predictions": self.total_predictions,
            "precision_score": self.precision_score,
            "recall_score": self.recall_score,
            "f1_score": self.f1_score,
            "sample_size_confidence": self.sample_size_confidence,
            "last_calculated": self.last_calculated.isoformat() if self.last_calculated else None,
        }

    def update_scores(self):
        """Recalculate precision/recall/F1 scores."""
        if self.true_positives + self.false_positives > 0:
            self.precision_score = self.true_positives / (self.true_positives + self.false_positives)
        else:
            self.precision_score = None

        # Recall requires ground truth which we may not have
        # F1 score calculated if both precision and recall available
        if self.precision_score and self.recall_score:
            if self.precision_score + self.recall_score > 0:
                self.f1_score = 2 * (self.precision_score * self.recall_score) / (self.precision_score + self.recall_score)

        # Confidence increases with sample size (logarithmic)
        import math
        if self.total_predictions > 0:
            self.sample_size_confidence = min(1.0, math.log10(self.total_predictions + 1) / 2)

        from datetime import datetime
        self.last_calculated = datetime.utcnow()
