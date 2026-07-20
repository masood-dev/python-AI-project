"""Pydantic schemas for document endpoints."""
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Schema for document response."""

    id: str = Field(..., alias="_id")
    session_id: str
    filename: str
    file_type: str
    uploaded_at: datetime

    class Config:
        """Pydantic config."""
        populate_by_name = True


class DocumentListResponse(BaseModel):
    """Schema for document list response."""

    documents: list[DocumentResponse]
    total: int
