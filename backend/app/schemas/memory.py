from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MemoryOut(BaseModel):
    id: UUID
    category: str
    title: str
    content: str
    importance_score: float
    approved: bool
    created_at: datetime

    class Config:
        from_attributes = True
