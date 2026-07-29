from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.mood import MoodEntry
from app.schemas.wellbeing import MoodCreate, MoodOut

router = APIRouter()


@router.post("/", response_model=MoodOut, status_code=201)
def log_mood(payload: MoodCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    entry = MoodEntry(user_id=current_user.id, source="manual", **payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=list[MoodOut])
def mood_history(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(MoodEntry)
        .filter(MoodEntry.user_id == current_user.id)
        .order_by(MoodEntry.created_at.desc())
        .limit(100)
        .all()
    )