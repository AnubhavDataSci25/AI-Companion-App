from app.services.ai_service import get_client
from app.models.memory import EMBEDDING_DIM


def embed_text(text: str) -> list[float]:
    client = get_client()
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    embedding = result.embeddings[0].values
    if len(embedding) != EMBEDDING_DIM:
        raise ValueError(f"Expected embedding dimension {EMBEDDING_DIM}, got {len(embedding)}")
    return embedding
