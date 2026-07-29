import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    source = Column(String, default="manual")  # "manual" or "ai_suggested"
    related_event_id = Column(UUID(as_uuid=True), ForeignKey("important_events.id"), nullable=True)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)