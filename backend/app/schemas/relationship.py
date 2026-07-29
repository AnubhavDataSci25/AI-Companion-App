from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ReminderCreate(BaseModel):
    title: str
    remind_at: datetime


class ReminderOut(BaseModel):
    id: UUID
    title: str
    remind_at: datetime
    source: str
    sent: bool

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    title: str
    event_type: str
    event_date: date
    notes: Optional[str] = None


class EventOut(BaseModel):
    id: UUID
    title: str
    event_type: str
    event_date: date
    notes: Optional[str]

    class Config:
        from_attributes = True


class SharedMemoryCreate(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    event_date: Optional[date] = None


class SharedMemoryOut(BaseModel):
    id: UUID
    title: str
    category: str
    description: Optional[str]
    event_date: Optional[date]

    class Config:
        from_attributes = True
