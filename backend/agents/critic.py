"""
Critic Agent
------------
Input: Resume text + GitHub summary
Output: List of red flags (JSON)
"""

from gemini_client import call_gemini
from utils.json_helper import parse_json


def run_critic(resume_text: str, github_summary: str = "") -> dict:
    prompt = f"""You are a critical hiring reviewer AI. Your job is to spot potential issues
that a careful human reviewer might catch in this resume.

Check specifically for:
- Keyword stuffing (skills listed but never demonstrated with a project/experience)
- Vague or generic project descriptions with no real detail
- Lack of deployed/live project links or GitHub repos for claimed projects
- Mismatch between claimed years of experience and depth of projects shown
- GitHub inactivity or very few/no public repositories (use the GitHub summary below)

Resume Text:
{resume_text}

GitHub Activity Summary:
{github_summary if github_summary else "Not provided"}

Return ONLY valid JSON, no markdown, in this exact format:
{{
  "red_flags": ["flag 1", "flag 2"]
}}

If you find no significant issues, return an empty list for "red_flags".
Keep each flag short (under 12 words).
"""
    raw = call_gemini(prompt)
    return parse_json(raw)
