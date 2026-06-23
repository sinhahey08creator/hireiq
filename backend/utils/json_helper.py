"""
Gemini sometimes wraps JSON in ```json ... ``` markdown fences.
This helper strips that and safely parses the JSON.
"""

import json


def parse_json(raw: str) -> dict:
    cleaned = raw.strip()

    # Remove markdown code fences if present
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: return raw text wrapped, so the app doesn't crash
        return {"error": "Could not parse AI response", "raw": raw}
