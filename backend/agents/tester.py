"""
Tester Agent
------------
Input: Matched skills (from Researcher)
Output: Interview questions (JSON)
"""

from gemini_client import call_gemini
from utils.json_helper import parse_json


def run_tester(matched_skills: list, difficulty: str = "Medium") -> dict:
    skills_list = ", ".join(matched_skills) if matched_skills else "General Software Development"

    prompt = f"""You are a technical interviewer AI.

Generate 5 interview questions to assess a candidate's depth of knowledge in: {skills_list}

Difficulty level: {difficulty}

Return ONLY valid JSON, no markdown, in this exact format:
{{
  "questions": ["question 1", "question 2", "question 3", "question 4", "question 5"]
}}
"""
    raw = call_gemini(prompt)
    return parse_json(raw)
