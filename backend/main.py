"""
HireIQ Backend — Main FastAPI App
==================================

Pipeline:
  Upload (JD + Resume + GitHub username)
    -> Planner Agent   (extracts required skills + weights from JD)
    -> Researcher Agent (matches resume/GitHub against required skills)
    -> Critic Agent     (finds red flags in resume/GitHub)
    -> Tester Agent     (generates interview questions for matched skills)
    -> Final Score      (combines everything into one recommendation)

Run with:
  uvicorn main:app --reload --port 8000
"""

import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from agents.planner import run_planner
from agents.researcher import run_researcher
from agents.critic import run_critic
from agents.tester import run_tester
from utils.pdf_parser import extract_text_from_pdf
from utils.github_fetch import get_github_summary

app = FastAPI(title="HireIQ API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hireiq-brown-three.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "HireIQ API is running"}


@app.post("/planner")
async def planner_endpoint(job_description: str = Form(...)):
    """Standalone endpoint — useful for testing the Planner agent alone."""
    return run_planner(job_description)


@app.post("/analyze")
async def analyze_endpoint(
    job_description: str = Form(...),
    github_username: str = Form(""),
    resume: UploadFile = File(...),
):
    """
    Main endpoint — runs the full 4-agent pipeline on one candidate.
    """

    # 1. Save uploaded PDF to a temp file and extract text
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(resume.file, tmp)
        tmp_path = tmp.name

    try:
        resume_text = extract_text_from_pdf(tmp_path)
    finally:
        os.remove(tmp_path)

    # 2. Fetch GitHub activity (optional)
    github_summary = get_github_summary(github_username) if github_username else ""

    # 3. Run agents in sequence
    planner_result = run_planner(job_description)
    required_skills = planner_result.get("skills", [])

    researcher_result = run_researcher(resume_text, required_skills, github_summary)

    critic_result = run_critic(resume_text, github_summary)

    matched_skills = researcher_result.get("matched", [])
    tester_result = run_tester(matched_skills)

    # 4. Compute final score
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
