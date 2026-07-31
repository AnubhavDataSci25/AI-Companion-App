from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str


class ChatMessageOut(BaseModel):
    id: UUID
    sender: str
    content: str
    mood: Optional[str] = None
    created_at: datetime
