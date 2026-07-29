from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class JournalCreate(BaseModel):
    title: Optional[str] = None
    content: str
    mood_label: Optional[str] = None


class JournalOut(BaseModel):
    id: UUID
    title: Optional[str]
    content: str
    mood_label: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MoodCreate(BaseModel):
    mood_label: str
    intensity: float = 0.5
    note: Optional[str] = None


class MoodOut(BaseModel):
    id: UUID
    mood_label: str
    intensity: float
    source: str
    note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
