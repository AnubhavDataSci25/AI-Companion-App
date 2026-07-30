import uuid

from sqlalchemy.orm import Session as DBSession

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.memory import Memory
from app.models.mood import MoodEntry
from app.services import ai_service
from app.services.memory_retrieval_service import retrieve_relevant_memories, format_memory_context
from app.services.memory_extraction_service import extract_memories, needs_consent
from app.services.embedding_service import embed_text
from app.services.mood_service import detect_mood


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

def _save_extracted_memories(db: DBSession, user_id: uuid.UUID, user_message: str, ami_reply: str):
    try:
        candidates = extract_memories(user_message, ami_reply)
    except Exception as e:
        print(f"[memory_extraction] Failed to extract memories: {e}")
        return

    for c in candidates:
        try:
            memory = Memory(
                user_id=user_id,
                category=c["category"],
                title=c["title"],
                content=c["content"],
                importance_score=float(c.get("importance_score", 0.5)),
                embedding=embed_text(c["content"]),
                approved=not needs_consent(c["category"]),  # sensitive categories wait for explicit approval
            )
            db.add(memory)
        except Exception as e:
            print(f"[memory_extraction] Skipping memory candidate: {e}")
            continue  # skip malformed extraction, never break chat

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[memory_extraction] Failed to save memories: {e}")

def send_message(db: DBSession, user_id: uuid.UUID, conversation_id: str | None, content: str):
    convo = get_or_create_conversation(db, user_id, conversation_id)

    user_msg = Message(conversation_id=convo.id, sender="user", content=content)
    db.add(user_msg)
    db.commit()

    mood_result = detect_mood(content)
    user_msg.mood = mood_result["mood_label"]
    db.add(MoodEntry(
        user_id=user_id,
        mood_label=mood_result["mood_label"],
        intensity=mood_result["intensity"],
        source="chat",
    ))
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

    relevant_memories = retrieve_relevant_memories(db, user_id, content)
    memory_context = format_memory_context(relevant_memories)

    reply_text = ai_service.generate_reply(db, gemini_history, memory_context=memory_context, current_mood=mood_result["mood_label"])

    ami_msg = Message(conversation_id=convo.id, sender="ami", content=reply_text)
    db.add(ami_msg)
    db.commit()
    db.refresh(ami_msg)

    _save_extracted_memories(db, user_id, content, reply_text)

    return convo, ami_msg
