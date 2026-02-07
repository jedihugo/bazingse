"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Any
from datetime import datetime


# Life Event schemas
class LifeEventCreate(BaseModel):
    """Schema for creating a life event."""
    year: int = Field(..., ge=1900, le=2100)
    month: Optional[int] = Field(None, ge=1, le=12)
    day: Optional[int] = Field(None, ge=1, le=31)
    location: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=10000)
    is_abroad: Optional[bool] = False


class LifeEventUpdate(BaseModel):
    """Schema for updating a life event."""
    year: Optional[int] = Field(None, ge=1900, le=2100)
    month: Optional[int] = Field(None, ge=1, le=12)
    day: Optional[int] = Field(None, ge=1, le=31)
    location: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=10000)
    is_abroad: Optional[bool] = None


class LifeEvent(BaseModel):
    """Schema for life event response."""
    id: str
    year: int
    month: Optional[int] = None
    day: Optional[int] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    is_abroad: Optional[bool] = False
    created_at: str
    updated_at: str


# Profile schemas
class ProfileCreate(BaseModel):
    """Schema for creating a profile."""
    name: str = Field(..., min_length=1, max_length=100)
    birth_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    birth_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")  # HH:MM or None
    gender: Literal["male", "female"]
    place_of_birth: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)  # Mobile/WhatsApp number
    life_events: Optional[List[Any]] = Field(default=None)


class ProfileUpdate(BaseModel):
    """Schema for updating a profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    birth_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    birth_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    gender: Optional[Literal["male", "female"]] = None
    place_of_birth: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    life_events: Optional[List[Any]] = Field(default=None)


class ProfileResponse(BaseModel):
    """Schema for profile API responses."""
    id: str
    name: str
    birth_date: str
    birth_time: Optional[str]
    gender: str
    place_of_birth: Optional[str] = None
    phone: Optional[str] = None
    life_events: Optional[List[LifeEvent]] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
