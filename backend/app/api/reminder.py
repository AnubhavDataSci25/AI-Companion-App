from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.reminder import Reminder
from app.schemas.relationship import ReminderCreate, ReminderOut

router = APIRouter()


@router.post("/", response_model=ReminderOut, status_code=201)
def create_reminder(payload: ReminderCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    reminder = Reminder(user_id=current_user.id, source="manual", **payload.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.get("/", response_model=list[ReminderOut])
def list_reminders(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Reminder)
        .filter(Reminder.user_id == current_user.id)
        .order_by(Reminder.remind_at.asc())
        .all()
    )


@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: str, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == current_user.id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    db.delete(reminder)
    db.commit()