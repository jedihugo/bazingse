
from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, init_db
from schemas import ProfileCreate, ProfileUpdate, ProfileResponse, LifeEventCreate, LifeEventUpdate, LifeEvent
import crud


# * =================
# * API ENDPOINTS
# * =================

router = APIRouter()


# * =================
# * PROFILE ENDPOINTS
# * =================

@router.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()


@router.post("/seed", status_code=201)
async def seed_database(db: Session = Depends(get_db)):
    """Seed the database with test profiles."""
    from models import Profile
    import uuid

    # Check if profiles already exist
    existing_count = db.query(Profile).count()
    if existing_count > 0:
        return {"message": f"Database already has {existing_count} profiles. Skipping seed."}

    # Test presets
    TEST_PRESETS = [
        {"date": "1969-07-04", "time": "18:20", "gender": "female", "name": "Test 1969-07-04"},
        {"date": "1992-07-06", "time": "09:30", "gender": "female", "name": "Test 1992-07-06"},
        {"date": "1995-04-19", "time": "17:30", "gender": "male", "name": "Test 1995-04-19"},
        {"date": "1985-06-23", "time": "13:30", "gender": "male", "name": "Test 1985-06-23"},
        {"date": "1988-02-02", "time": "13:30", "gender": "male", "name": "Test 1988-02-02"},
        {"date": "1986-11-29", "time": "13:30", "gender": "male", "name": "Test 1986-11-29"},
        {"date": "1995-08-14", "time": "11:30", "gender": "female", "name": "Test 1995-08-14"},
        {"date": "1995-07-18", "time": "16:30", "gender": "female", "name": "Test 1995-07-18"},
        {"date": "1992-09-18", "time": "09:30", "gender": "female", "name": "Test 1992-09-18"},
        {"date": "2002-04-17", "time": "08:20", "gender": "female", "name": "Test 2002-04-17"},
        {"date": "2019-09-18", "time": "05:00", "gender": "female", "name": "Test 2019-09-18"},
        {"date": "2021-08-09", "time": "21:00", "gender": "female", "name": "Test 2021-08-09"},
        {"date": "1985-03-20", "time": "23:00", "gender": "female", "name": "Test 1985-03-20"},
        {"date": "1995-02-10", "time": "10:10", "gender": "female", "name": "Test 1995-02-10"},
        {"date": "1946-08-12", "time": "07:00", "gender": "male", "name": "Suharsa"},
        {"date": "1962-11-03", "time": "11:45", "gender": "male", "name": "Malaysian - Mata Ikan"},
        {"date": "1954-02-09", "time": "09:30", "gender": "female", "name": "Test 1954-02-09"},
        {"date": "1949-12-19", "time": "08:00", "gender": "male", "name": "Test 1949-12-19"},
        {"date": "1955-10-18", "time": "20:00", "gender": "female", "name": "Test 1955-10-18"},
        {"date": "1992-12-25", "time": None, "gender": "female", "name": "Test 1992-12-25 (Unknown Hour)"},
        {"date": "1945-03-26", "time": "18:00", "gender": "male", "name": "Batubara (hutan, tanah, pulau)"},
        {"date": "1969-04-07", "time": "18:30", "gender": "female", "name": "Wu Chen Wealth Storage"},
    ]

    # Add test profiles
    for preset in TEST_PRESETS:
        profile = Profile(
            id=str(uuid.uuid4()),
            name=preset["name"],
            birth_date=preset["date"],
            birth_time=preset["time"],
            gender=preset["gender"],
        )
        db.add(profile)

    db.commit()
    return {"message": f"Successfully seeded {len(TEST_PRESETS)} profiles."}


@router.get("/profiles", response_model=List[ProfileResponse])
async def list_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=10000),
    db: Session = Depends(get_db)
):
    """List all profiles."""
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles


@router.post("/profiles", response_model=ProfileResponse, status_code=201)
async def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    """Create a new profile."""
    profile = crud.create_profile(db, profile_data)
    return profile


@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """Get a single profile by ID."""
    profile = crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: str,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing profile."""
    profile = crud.update_profile(db, profile_id, profile_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.delete("/profiles/{profile_id}", status_code=204)
async def delete_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """Delete a profile."""
    success = crud.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return None


# * =================
# * LIFE EVENT ENDPOINTS
# * =================

@router.post("/profiles/{profile_id}/life_events", response_model=LifeEvent, status_code=201)
async def create_life_event(
    profile_id: str,
    event_data: LifeEventCreate,
    db: Session = Depends(get_db)
):
    """Create a new life event for a profile."""
    event = crud.add_life_event(db, profile_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Profile not found")
    return event


@router.get("/profiles/{profile_id}/life_events/{event_id}", response_model=LifeEvent)
async def get_life_event(
    profile_id: str,
    event_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific life event."""
    event = crud.get_life_event(db, profile_id, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Life event not found")
    return event


@router.put("/profiles/{profile_id}/life_events/{event_id}", response_model=LifeEvent)
async def update_life_event(
    profile_id: str,
    event_id: str,
    event_data: LifeEventUpdate,
    db: Session = Depends(get_db)
):
    """Update a life event."""
    event = crud.update_life_event(db, profile_id, event_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Life event not found")
    return event


@router.delete("/profiles/{profile_id}/life_events/{event_id}", status_code=204)
async def delete_life_event(
    profile_id: str,
    event_id: str,
    db: Session = Depends(get_db)
):
    """Delete a life event."""
    success = crud.delete_life_event(db, profile_id, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Life event not found")
    return None
