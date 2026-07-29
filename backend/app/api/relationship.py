from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.profile import ImportantEvent
from app.models.shared_memory import SharedMemory
from app.schemas.relationship import EventCreate, EventOut, SharedMemoryCreate, SharedMemoryOut

router = APIRouter()


@router.post("/events", response_model=EventOut, status_code=201)
def create_event(payload: EventCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = ImportantEvent(user_id=current_user.id, **payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events", response_model=list[EventOut])
def list_events(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(ImportantEvent)
        .filter(ImportantEvent.user_id == current_user.id)
        .order_by(ImportantEvent.event_date.asc())
        .all()
    )


@router.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: str, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(ImportantEvent).filter(ImportantEvent.id == event_id, ImportantEvent.user_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    db.delete(event)
    db.commit()


@router.post("/shared-memories", response_model=SharedMemoryOut, status_code=201)
def create_shared_memory(payload: SharedMemoryCreate, db: DBSession = Depends(get_db), _: User = Depends(get_current_user)):
    entry = SharedMemory(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/shared-memories", response_model=list[SharedMemoryOut])
def list_shared_memories(db: DBSession = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(SharedMemory).order_by(SharedMemory.event_date.asc().nulls_last()).all()


@router.get("/timeline")
def get_timeline(db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Combines important_events and shared_memories into a single date-sorted timeline."""
    events = db.query(ImportantEvent).filter(ImportantEvent.user_id == current_user.id).all()
    memories = db.query(SharedMemory).all()

    timeline = [
        {"type": "event", "title": e.title, "date": e.event_date.isoformat(), "notes": e.notes, "event_type": e.event_type}
        for e in events
    ] + [
        {"type": "shared_memory", "title": m.title, "date": m.event_date.isoformat() if m.event_date else None,
         "notes": m.description, "category": m.category}
        for m in memories
    ]

    timeline.sort(key=lambda x: x["date"] or "9999-99-99")
    return timeline