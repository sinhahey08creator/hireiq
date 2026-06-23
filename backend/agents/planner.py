"""
Planner Agent
-------------
Input: Job Description (text)
Output: Required skills + weightage (JSON)
"""

from gemini_client import call_gemini
from utils.json_helper import parse_json


def run_planner(job_description: str) -> dict:
    prompt = f"""You are a hiring planner AI.

Analyze the following Job Description and extract:
1. The required skills/competencies
2. A weightage (out of 100, all weights summing to 100) for each skill based on importance for this role

Return ONLY valid JSON, no markdown, no explanation, in this exact format:
{{
  "skills": [
    {{"name": "Skill Name", "weight": 30}}
  ]
}}

Job Description:
{job_description}
"""
    raw = call_gemini(prompt)
    return parse_json(raw)
