import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class SharedMemory(Base):
    __tablename__ = "shared_memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # trip, celebration, important_place, inside_joke, milestone
    description = Column(String, nullable=True)
    event_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)