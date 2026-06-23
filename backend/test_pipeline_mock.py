"""
MOCK PIPELINE TEST
===================
This script tests the ENTIRE HireIQ pipeline logic (PDF parsing -> agents ->
JSON parsing -> scoring -> recommendation) WITHOUT calling the real Gemini API.

We fake Gemini's responses with a simple keyword-matching "brain" so we can verify:
  1. No code crashes anywhere in the pipeline
  2. PDF text extraction works on all 6 sample resumes
  3. JSON parsing handles Gemini's typical response format correctly
  4. Final score + recommendation math works correctly
  5. Edge cases (missing GitHub, empty fields) don't break anything

IMPORTANT: This does NOT test whether the AI's judgment is good — that requires
a real Gemini API key. This only proves the surrounding code is solid.

Run with:  python test_pipeline_mock.py
"""

import os
import re
import json
import sys

# Dummy key so gemini_client.py doesn't raise an error on import
os.environ["GEMINI_API_KEY"] = "dummy-key-for-testing"

import gemini_client  # noqa: E402


# ─────────────────────────────────────────────
# FAKE GEMINI BRAIN — simple keyword-based mock
# ─────────────────────────────────────────────
def fake_call_gemini(prompt: str) -> str:
    """
    Looks at the prompt to figure out which agent is calling, then returns
    a plausible JSON string — same shape real Gemini would return.
    """

    # ---- PLANNER ----
    if "hiring planner" in prompt.lower():
        skills_found = re.findall(r"^[A-Za-z][A-Za-z0-9./+ ]{1,30}$", prompt, re.MULTILINE)
        # crude heuristic: just hardcode a few based on common JD keywords present
        candidates = ["React", "Node.js", "MongoDB", "Git", "Python", "Django",
                      "PostgreSQL", "Docker", "AWS", "Kubernetes", "SQL", "Power BI",
                      "Figma", "JavaScript", "CSS", "Communication"]
        found = [s for s in candidates if s.lower() in prompt.lower()]
        if not found:
            found = ["Communication"]
        weight = round(100 / len(found))
        skills = [{"name": s, "weight": weight} for s in found]
        return json.dumps({"skills": skills})

    # ---- RESEARCHER ----
    if "hiring researcher" in prompt.lower():
        # crude overlap check between "Required Skills:" line and resume text
        req_match = re.search(r"Required Skills:\s*(.*)", prompt)
        required = [s.strip() for s in req_match.group(1).split(",")] if req_match else []
        resume_section = prompt.split("Resume Text:")[-1].split("GitHub Activity")[0].lower()

        matched, missing = [], []
        for skill in required:
            if skill.lower() in resume_section:
                matched.append(skill)
            else:
                missing.append(skill)

        score = round((len(matched) / len(required)) * 100) if required else 50
        return json.dumps({"score": score, "matched": matched, "missing": missing})

    # ---- CRITIC ----
    if "critical hiring reviewer" in prompt.lower():
        resume_section = prompt.split("Resume Text:")[-1].lower()
        flags = []
        vague_words = ["modern tech stack", "many features", "various projects",
                        "great ui/ux", "advanced features"]
        for vw in vague_words:
            if vw in resume_section:
                flags.append("Vague, non-specific project description")
                break
        if "github.com" not in resume_section:
            flags.append("No GitHub or project links provided")
        buzzword_count = sum(
            1 for kw in ["blockchain", "machine learning", "tensorflow", "kubernetes", "data science"]
            if kw in resume_section
        )
        if buzzword_count >= 3:
            flags.append("Possible keyword stuffing — many unrelated buzzwords")
        return json.dumps({"red_flags": flags})

    # ---- TESTER ----
    if "technical interviewer" in prompt.lower():
        return json.dumps({
            "questions": [
                "Explain the core concepts behind your strongest listed skill.",
                "Walk me through a challenging bug you fixed recently.",
                "How do you approach testing your code?",
                "Describe a project where you collaborated with a team.",
                "What would you improve about your most recent project?",
            ]
        })

    return json.dumps({"error": "Unrecognized prompt type in mock"})


# Patch BEFORE importing agents, so they pick up the mocked version
gemini_client.call_gemini = fake_call_gemini

# Now import the rest of the pipeline (agents will use the patched function)
sys.path.insert(0, os.path.dirname(__file__))
from agents.planner import run_planner          # noqa: E402
from agents.researcher import run_researcher    # noqa: E402
from agents.critic import run_critic            # noqa: E402
from agents.tester import run_tester            # noqa: E402
from utils.pdf_parser import extract_text_from_pdf  # noqa: E402


# ─────────────────────────────────────────────
# TEST CASES (matches TEST_GUIDE.md)
# ─────────────────────────────────────────────
TEST_CASES = [
    {
        "name": "Test 1 — Happy Path (Strong Full Stack)",
        "jd": "../test_data/job_descriptions/JD1_fullstack_developer.txt",
        "resume": "../test_data/resumes/01_strong_fullstack_priya.pdf",
    },
    {
        "name": "Test 2 — Red Flags (Weak / Keyword Stuffing)",
        "jd": "../test_data/job_descriptions/JD1_fullstack_developer.txt",
        "resume": "../test_data/resumes/02_weak_redflags_rahul.pdf",
    },
    {
        "name": "Test 3 — Strong Match, Data Analyst",
        "jd": "../test_data/job_descriptions/JD2_data_analyst.txt",
        "resume": "../test_data/resumes/03_strong_dataanalyst_ananya.pdf",
    },
    {
        "name": "Test 4 — Skill Mismatch (Frontend resume vs Backend JD)",
        "jd": "../test_data/job_descriptions/JD3_backend_developer.txt",
        "resume": "../test_data/resumes/04_mismatch_backend_sara.pdf",
    },
    {
        "name": "Test 5 — Strong Match, Frontend",
        "jd": "../test_data/job_descriptions/JD4_frontend_developer.txt",
        "resume": "../test_data/resumes/05_strong_frontend_karan.pdf",
    },
    {
        "name": "Test 6 — Average Candidate, Partial Gaps",
        "jd": "../test_data/job_descriptions/JD5_devops_engineer.txt",
        "resume": "../test_data/resumes/06_average_devops_vikram.pdf",
    },
]


def run_full_pipeline(jd_path, resume_path):
    """Mirrors the exact logic in main.py's /analyze endpoint."""
    with open(jd_path, "r") as f:
        job_description = f.read()

    resume_text = extract_text_from_pdf(resume_path)
    github_summary = ""  # skipping live GitHub calls in this mock test

    planner_result = run_planner(job_description)
    required_skills = planner_result.get("skills", [])

    researcher_result = run_researcher(resume_text, required_skills, github_summary)
    critic_result = run_critic(resume_text, github_summary)

    matched_skills = researcher_result.get("matched", [])
    tester_result = run_tester(matched_skills)

    base_score = researcher_result.get("score", 0)
    red_flag_penalty = len(critic_result.get("red_flags", [])) * 5
    final_score = max(0, min(100, base_score - red_flag_penalty))

    if final_score >= 75:
        recommendation = "Strongly Recommended"
    elif final_score >= 50:
        recommendation = "Recommended with Reservations"
    else:
        recommendation = "Not Recommended"

    return {
        "planner": planner_result,
        "researcher": researcher_result,
        "critic": critic_result,
        "tester": tester_result,
        "final_score": final_score,
        "recommendation": recommendation,
    }


# ─────────────────────────────────────────────
# RUN ALL TESTS
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("HIREIQ MOCK PIPELINE TEST — verifying code logic (not AI quality)")
    print("=" * 70)

    all_passed = True

    for case in TEST_CASES:
        print(f"\n--- {case['name']} ---")
        try:
            result = run_full_pipeline(case["jd"], case["resume"])

            print(f"  Planner skills found : {len(result['planner'].get('skills', []))}")
            print(f"  Researcher score      : {result['researcher'].get('score')}")
            print(f"  Matched skills        : {result['researcher'].get('matched')}")
            print(f"  Missing skills        : {result['researcher'].get('missing')}")
            print(f"  Critic red flags      : {result['critic'].get('red_flags')}")
            print(f"  Tester questions      : {len(result['tester'].get('questions', []))} generated")
            print(f"  FINAL SCORE           : {result['final_score']} / 100")
            print(f"  RECOMMENDATION        : {result['recommendation']}")

            # Basic sanity checks
            assert isinstance(result["final_score"], int), "final_score must be an int"
            assert 0 <= result["final_score"] <= 100, "final_score out of range"
            assert len(result["tester"].get("questions", [])) == 5, "expected 5 questions"
            print("  ✅ PASSED sanity checks")

        except Exception as e:
            all_passed = False
            print(f"  ❌ FAILED: {type(e).__name__}: {e}")

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL 6 TEST CASES RAN WITHOUT CRASHING. Pipeline logic is solid.")
        print("   Next step: plug in a real GEMINI_API_KEY and re-test for AI quality.")
    else:
        print("❌ SOME TESTS FAILED — see errors above.")
    print("=" * 70)
