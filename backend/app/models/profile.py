import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)

    # Identity
    nickname = Column(String, nullable=True)
    pronouns = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    language = Column(String, nullable=True)
    timezone = Column(String, nullable=True)

    # Communication
    communication_style = Column(String, nullable=True)
    love_language = Column(String, nullable=True)
    humor_preference = Column(String, nullable=True)

    # Interests (stored as flexible JSON — hobbies, music, movies, books, food, color)
    interests = Column(JSONB, nullable=True)

    # Preferences
    topics_to_avoid = Column(JSONB, nullable=True)
    theme_preference = Column(String, nullable=True)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RelationshipProfile(Base):
    __tablename__ = "relationship_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    developer_name = Column(String, nullable=True)
    partner_name = Column(String, nullable=True)
    anniversary = Column(Date, nullable=True)
    nicknames = Column(JSONB, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ImportantEvent(Base):
    __tablename__ = "important_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # birthday, anniversary, exam, appointment, custom
    event_date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)