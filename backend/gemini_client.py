"""
Shared Gemini client used by all 4 agents.
Each "agent" is just this function called with a different prompt.

Uses the official `google-genai` SDK (the old `google-generativeai` package
is deprecated as of 2025 — do not switch back to it).
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Copy .env.example to .env and add your key."
    )

client = genai.Client(api_key=api_key)

# Free-tier, fast model. Change here if you want to use a different one.
MODEL_NAME = "gemini-2.5-flash"


def call_gemini(prompt: str) -> str:
    """Sends a prompt to Gemini and returns the raw text response."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text
