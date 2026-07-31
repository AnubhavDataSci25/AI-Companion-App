from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.journal import JournalEntry
from app.schemas.wellbeing import JournalCreate, JournalOut

router = APIRouter()


@router.post("/", response_model=JournalOut, status_code=201)
def create_entry(payload: JournalCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    entry = JournalEntry(user_id=current_user.id, **payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=list[JournalOut])
def list_entries(limit: int=50, offset: int = 0, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    limit = min(limit, 100)
    return (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == current_user.id)
        .order_by(JournalEntry.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )