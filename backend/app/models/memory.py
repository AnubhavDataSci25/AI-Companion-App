import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from app.core.database import Base

EMBEDDING_DIM = 3072  # Gemini embedding output size


class Memory(Base):
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)  # personal_profile, relationship, events, preferences, health, goals, habits, journal_insights
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    importance_score = Column(Float, default=0.5)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=True)
    approved = Column(Boolean, default=False)  # consent gate — not usable in context until approved
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
