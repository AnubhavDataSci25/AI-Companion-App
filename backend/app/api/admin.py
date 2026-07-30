from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.user import User
from app.models.setting import Setting
from app.models.admin_log import AdminLog
from app.models.memory import Memory
from app.schemas.admin import PersonalityUpdate, FeatureFlagsUpdate, AdminLogOut, SettingOut
from app.schemas.memory import MemoryOut
from app.services.audit_service import log_admin_action

router = APIRouter()


def _upsert_setting(db: DBSession, key: str, value: dict) -> Setting:
    row = db.query(Setting).filter(Setting.key == key).first()
    if row:
        row.value = value
    else:
        row = Setting(key=key, value=value)
        db.add(row)
    db.commit()
    db.refresh(row)
    return row


# --- Personality / Prompt editor ---

@router.get("/personality", response_model=SettingOut)
def get_personality(db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    row = db.query(Setting).filter(Setting.key == "ami_personality_prompt").first()
    if not row:
        raise HTTPException(status_code=404, detail="No custom personality set — Ami is using the default.")
    return row


@router.put("/personality", response_model=SettingOut)
def update_personality(payload: PersonalityUpdate, db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    row = _upsert_setting(db, "ami_personality_prompt", {"text": payload.text})
    log_admin_action(db, admin.id, "updated_personality_prompt", payload.text[:200])
    return row


# --- Feature flags ---

@router.get("/feature-flags", response_model=SettingOut)
def get_feature_flags(db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    row = db.query(Setting).filter(Setting.key == "feature_flags").first()
    if not row:
        row = _upsert_setting(db, "feature_flags", {"journal": True, "mood_tracking": True, "reminders": True})
    return row


@router.put("/feature-flags", response_model=SettingOut)
def update_feature_flags(payload: FeatureFlagsUpdate, db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    row = _upsert_setting(db, "feature_flags", payload.flags)
    log_admin_action(db, admin.id, "updated_feature_flags", str(payload.flags))
    return row


# --- Audit logs ---

@router.get("/logs", response_model=list[AdminLogOut])
def get_logs(db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(AdminLog).order_by(AdminLog.created_at.desc()).limit(200).all()


# --- Cross-user memory management (admin can view/edit partner's memories with their consent workflow intact) ---

@router.get("/memories/{user_id}", response_model=list[MemoryOut])
def get_user_memories(user_id: str, db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(Memory).filter(Memory.user_id == user_id).order_by(Memory.created_at.desc()).all()


@router.delete("/memories/{memory_id}", status_code=204)
def admin_delete_memory(memory_id: str, db: DBSession = Depends(get_db), admin: User = Depends(require_admin)):
    memory = db.query(Memory).filter(Memory.id == memory_id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found.")
    db.delete(memory)
    log_admin_action(db, admin.id, "deleted_memory", memory_id)
    db.commit()