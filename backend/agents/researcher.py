"""
Researcher Agent
----------------
Input: Resume text + Planner's required skills + GitHub summary
Output: Match score, matched skills, missing skills (JSON)
"""

from gemini_client import call_gemini
from utils.json_helper import parse_json


def run_researcher(resume_text: str, required_skills: list, github_summary: str = "") -> dict:
    skills_list = ", ".join([s.get("name", "") for s in required_skills]) or "Not specified"

    prompt = f"""You are a hiring researcher AI.

Compare the candidate's resume (and GitHub activity, if provided) against the required skills for this role.

Required Skills: {skills_list}

Resume Text:
{resume_text}

GitHub Activity Summary:
{github_summary if github_summary else "Not provided"}

Return ONLY valid JSON, no markdown, in this exact format:
{{
  "score": 85,
  "matched": ["Skill1", "Skill2"],
  "missing": ["Skill3"]
}}

"score" should be an overall match percentage (0-100) based on how well the
resume and GitHub activity demonstrate the required skills.
"""
    raw = call_gemini(prompt)
    return parse_json(raw)
