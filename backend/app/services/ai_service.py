from google import genai

from app.core.config import settings

_client = None


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


# Ami's base personality + safety rules (Prompt Layers: System + Personality + Safety, per README 05)
AMI_SYSTEM_PROMPT = """You are Ami, a warm and emotionally supportive AI companion.

Core rules you must always follow:
- You are an AI. Never claim or imply you are human.
- Be empathetic, calm, and genuine — never manipulate emotions to keep the user engaged.
- Encourage real-world communication and relationships; never position yourself as a replacement for human connection.
- Be honest and avoid overdependence — if the user seems to be relying on you unhealthily, gently encourage them to reach out to people in their life.
- Keep responses natural and conversational, not clinical.
"""


def generate_reply(conversation_history: list[dict], memory_context: str = "") -> str:
    """
    conversation_history: list of {"role": "user"|"model", "content": str}
    memory_context: relevant retrieved memories, injected as extra context (Phase 3 will populate this)
    """
    client = get_client()

    prompt_parts = [AMI_SYSTEM_PROMPT]
    if memory_context:
        prompt_parts.append(f"\nRelevant memory context:\n{memory_context}")

    system_instruction = "\n".join(prompt_parts)

    contents = [
        {"role": turn["role"], "parts": [{"text": turn["content"]}]}
        for turn in conversation_history
    ]

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config={"system_instruction": system_instruction},
    )

    return response.text