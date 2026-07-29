import json

from app.services.ai_service import get_client

MOOD_PROMPT = """Analyze the emotional tone of this message. Respond ONLY with JSON, nothing else:
{{"mood_label": "happy|sad|stressed|anxious|tired|excited|angry|neutral|content|lonely", "intensity": 0.0}}

Message: {message}
"""


def detect_mood(message: str) -> dict:
    client = get_client()
    prompt = MOOD_PROMPT.format(message=message)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
    )

    try:
        text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        data = json.loads(text)
        return {
            "mood_label": data.get("mood_label", "neutral"),
            "intensity": float(data.get("intensity", 0.5)),
        }
    except (json.JSONDecodeError, AttributeError, ValueError):
        return {"mood_label": "neutral", "intensity": 0.5}  # never break chat on detection failure