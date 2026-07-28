import json
import re

from app.services.ai_service import get_client

SENSITIVE_CATEGORIES = {"health"}

EXTRACTION_PROMPT = """From the exchange below, extract any durable facts worth remembering long-term
(preferences, milestones, important dates, goals, personal facts, relationship details).
Only extract clearly stated facts — never invent or infer beyond what was said.
If nothing is worth remembering, return an empty list.

Respond ONLY with JSON in this exact format, nothing else:
{{
  "memories": [
    {{"category": "personal_profile|relationship|events|preferences|health|goals|habits|journal_insights",
      "title": "short title",
      "content": "the fact, in one sentence",
      "importance_score": 0.0}}
  ]
}}

User said: {user_message}
Ami replied: {ami_reply}
"""


def _extract_json_payload(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def extract_memories(user_message: str, ami_reply: str) -> list[dict]:
    client = get_client()
    prompt = EXTRACTION_PROMPT.format(user_message=user_message, ami_reply=ami_reply)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        config={"response_mime_type": "application/json"},
    )

    try:
        data = _extract_json_payload(response.text)
        memories = data.get("memories", [])
        if not isinstance(memories, list):
            print(f"[memory_extraction] Expected memories list, got: {type(memories).__name__}")
            return []
        return memories
    except (json.JSONDecodeError, AttributeError, TypeError) as e:
        print(f"[memory_extraction] Failed to parse Gemini output: {e}")
        print(f"[memory_extraction] Raw response was: {response.text!r}")
        return []  # extraction failure should never break the chat flow


def needs_consent(category: str) -> bool:
    return category in SENSITIVE_CATEGORIES
