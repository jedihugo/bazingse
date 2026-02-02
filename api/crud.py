"""CRUD operations for profiles."""

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import Optional, List
from datetime import datetime
import uuid

from models import Profile
from schemas import ProfileCreate, ProfileUpdate, LifeEventCreate, LifeEventUpdate


def create_profile(db: Session, profile_data: ProfileCreate) -> Profile:
    """Create a new profile."""
    profile = Profile(
        id=str(uuid.uuid4()),
        name=profile_data.name,
        birth_date=profile_data.birth_date,
        birth_time=profile_data.birth_time,
        gender=profile_data.gender,
        place_of_birth=profile_data.place_of_birth,
        life_events=[],
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, profile_id: str) -> Optional[Profile]:
    """Get a profile by ID."""
    return db.query(Profile).filter(Profile.id == profile_id).first()


def get_profiles(db: Session, skip: int = 0, limit: int = 100) -> List[Profile]:
    """Get all profiles with pagination."""
    return db.query(Profile).offset(skip).limit(limit).all()


def update_profile(db: Session, profile_id: str, profile_data: ProfileUpdate) -> Optional[Profile]:
    """Update an existing profile."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return None

    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(db: Session, profile_id: str) -> bool:
    """Delete a profile by ID."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return False

    db.delete(profile)
    db.commit()
    return True


# Life Event CRUD operations

def add_life_event(db: Session, profile_id: str, event_data: LifeEventCreate) -> Optional[dict]:
    """Add a life event to a profile."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return None

    now = datetime.utcnow().isoformat()
    event = {
        "id": str(uuid.uuid4()),
        "year": event_data.year,
        "month": event_data.month,
        "day": event_data.day,
        "location": event_data.location,
        "notes": event_data.notes,
        "created_at": now,
        "updated_at": now,
    }

    # Initialize life_events if None
    if profile.life_events is None:
        profile.life_events = []

    # Append to list
    profile.life_events = profile.life_events + [event]

    # Flag as modified for SQLAlchemy to detect JSON mutation
    flag_modified(profile, 'life_events')

    db.commit()
    db.refresh(profile)
    return event


def update_life_event(
    db: Session, profile_id: str, event_id: str, event_data: LifeEventUpdate
) -> Optional[dict]:
    """Update a life event in a profile."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile or not profile.life_events:
        return None

    # Find and update the event
    updated_event = None
    events = list(profile.life_events)  # Create a copy

    for i, event in enumerate(events):
        if event.get("id") == event_id:
            update_data = event_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                events[i][field] = value
            events[i]["updated_at"] = datetime.utcnow().isoformat()
            updated_event = events[i]
            break

    if not updated_event:
        return None

    profile.life_events = events
    flag_modified(profile, 'life_events')

    db.commit()
    db.refresh(profile)
    return updated_event


def delete_life_event(db: Session, profile_id: str, event_id: str) -> bool:
    """Delete a life event from a profile."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile or not profile.life_events:
        return False

    # Filter out the event
    original_length = len(profile.life_events)
    events = [e for e in profile.life_events if e.get("id") != event_id]

    if len(events) == original_length:
        return False  # Event not found

    profile.life_events = events
    flag_modified(profile, 'life_events')

    db.commit()
    return True


def get_life_event(db: Session, profile_id: str, event_id: str) -> Optional[dict]:
    """Get a specific life event from a profile."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile or not profile.life_events:
        return None

    for event in profile.life_events:
        if event.get("id") == event_id:
            return event

    return None
