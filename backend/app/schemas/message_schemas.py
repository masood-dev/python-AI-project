"""Pydantic schemas for message endpoints."""
from datetime import datetime
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """Schema for creating a message."""

    content: str = Field(..., min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    """Schema for message response."""

    id: str = Field(..., alias="_id")
    session_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        """Pydantic config."""
        populate_by_name = True


class MessageListResponse(BaseModel):
    """Schema for message list response."""

    messages: list[MessageResponse]
    total: int


class ChatResponse(BaseModel):
    """Schema for chat response (user message + AI reply)."""

    user_message: MessageResponse
    assistant_message: MessageResponse
