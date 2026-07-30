from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)  # e.g. "ami_personality_prompt", "feature_flags"
    value = Column(JSONB, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)