from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
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