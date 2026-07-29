import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class MoodEntry(Base):
    __tablename__ = "moods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    mood_label = Column(String, nullable=False)  # e.g. happy, stressed, tired, excited, sad, neutral
    intensity = Column(Float, default=0.5)  # 0.0-1.0
    source = Column(String, default="chat")  # "chat" (auto-detected) or "manual" (self-logged)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)