from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class PersonalityUpdate(BaseModel):
    text: str


class FeatureFlagsUpdate(BaseModel):
    flags: dict[str, bool]


class AdminLogOut(BaseModel):
    id: UUID
    action: str
    detail: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SettingOut(BaseModel):
    key: str
    value: Any
    updated_at: datetime

    class Config:
        from_attributes = True
