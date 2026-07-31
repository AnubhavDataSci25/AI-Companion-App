from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.message import Message
from app.models.conversation import Conversation
from app.schemas.chat import ChatMessageOut, ChatRequest, ChatResponse
from app.services import chat_service

router = APIRouter()


@router.post("/send", response_model=ChatResponse)
def send(
    payload: ChatRequest,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        convo, ami_msg = chat_service.send_message(
            db, current_user.id, payload.conversation_id, payload.message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ami couldn't respond: {str(e)}")

    return ChatResponse(conversation_id=str(convo.id), reply=ami_msg.content)

@router.get("/{conversation_id}/messages", response_model=list[ChatMessageOut])
def get_messages(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    convo = db.query(Conversation).filter(
        Conversation.id == conversation_id, Conversation.user_id == current_user.id
    ).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found.")
 
    limit = min(limit, 100)
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    messages.reverse()  # return oldest-first for natural chat rendering
    return messages
