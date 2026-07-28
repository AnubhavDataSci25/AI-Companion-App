import uuid

from sqlalchemy.orm import Session as DBSession

from app.models.memory import Memory
from app.services.embedding_service import embed_text


def retrieve_relevant_memories(db: DBSession, user_id: uuid.UUID, query: str, top_k: int = 5) -> list[Memory]:
    query_embedding = embed_text(query)

    # cosine_distance: lower = more similar. Only approved memories are usable in context (consent gate).
    results = (
        db.query(Memory)
        .filter(Memory.user_id == user_id, Memory.approved == True)  # noqa: E712
        .filter(Memory.embedding.isnot(None))
        .order_by(Memory.embedding.cosine_distance(query_embedding))
        .limit(top_k * 2)  # overfetch, then re-rank below
        .all()
    )

    # Blend similarity rank with importance_score (recency already influences created_at ordering via ties)
    results.sort(key=lambda m: -(m.importance_score or 0.5))
    return results[:top_k]


def format_memory_context(memories: list[Memory]) -> str:
    if not memories:
        return ""
    lines = [f"- [{m.category}] {m.title}: {m.content}" for m in memories]
    return "\n".join(lines)