"""Pydantic schemas for session endpoints."""
from datetime import datetime
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema for creating a new session."""

    title: str = Field(..., min_length=1, max_length=255)


class SessionResponse(BaseModel):
    """Schema for session response."""

    id: str = Field(..., alias="_id")
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        populate_by_name = True


class SessionListResponse(BaseModel):
    """Schema for session list response."""

    sessions: list[SessionResponse]
    total: int
    page: int
    page_size: int
