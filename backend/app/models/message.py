import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # "user" or "ami"
    content = Column(String, nullable=False)
    tokens = Column(Integer, nullable=True)
    mood = Column(String, nullable=True)
    summary_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)