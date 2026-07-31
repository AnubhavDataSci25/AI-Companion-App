from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.memory import Memory
from app.schemas.memory import MemoryOut

router = APIRouter()


@router.get("/", response_model=list[MemoryOut])
def list_memories(limit: int=50, offset: int = 0, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    limit = min(limit, 100)
    return db.query(Memory).filter(Memory.user_id == current_user.id).order_by(Memory.created_at.desc()).offset(offset).limit(limit).all()


@router.post("/{memory_id}/approve", response_model=MemoryOut)
def approve_memory(memory_id: str, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    memory = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == current_user.id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found.")
    memory.approved = True
    db.commit()
    db.refresh(memory)
    return memory


@router.delete("/{memory_id}", status_code=204)
def delete_memory(memory_id: str, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    memory = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == current_user.id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found.")
    db.delete(memory)
    db.commit()