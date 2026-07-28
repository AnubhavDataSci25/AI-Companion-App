import uuid

from sqlalchemy.orm import Session as DBSession

from app.models.conversation import Conversation
from app.models.message import Message
from app.services import ai_service


def get_or_create_conversation(db: DBSession, user_id: uuid.UUID, conversation_id: str | None) -> Conversation:
    if conversation_id:
        convo = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if convo:
            return convo

    convo = Conversation(user_id=user_id)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return convo


def send_message(db: DBSession, user_id: uuid.UUID, conversation_id: str | None, content: str):
    convo = get_or_create_conversation(db, user_id, conversation_id)

    user_msg = Message(conversation_id=convo.id, sender="user", content=content)
    db.add(user_msg)
    db.commit()

    # Build conversation history for Gemini (last 20 messages, simple cap for now)
    history = (
        db.query(Message)
        .filter(Message.conversation_id == convo.id)
        .order_by(Message.created_at.asc())
        .limit(20)
        .all()
    )
    gemini_history = [
        {"role": "user" if m.sender == "user" else "model", "content": m.content}
        for m in history
    ]

    reply_text = ai_service.generate_reply(gemini_history)

    ami_msg = Message(conversation_id=convo.id, sender="ami", content=reply_text)
    db.add(ami_msg)
    db.commit()
    db.refresh(ami_msg)

    return convo, ami_msg