import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    partner = "partner"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    pin_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)