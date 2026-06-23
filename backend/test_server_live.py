"""
Starts the real FastAPI server in-process and sends a real HTTP request
to /analyze with an actual resume PDF file upload -- exactly like the
React frontend will. Uses the mock Gemini brain (no real API key needed).
"""
import os
os.environ["GEMINI_API_KEY"] = "dummy-key-for-testing"

import gemini_client
from test_pipeline_mock import fake_call_gemini
gemini_client.call_gemini = fake_call_gemini

# Re-patch agents too since main.py imports them fresh
import agents.planner, agents.researcher, agents.critic, agents.tester
agents.planner.call_gemini = fake_call_gemini
agents.researcher.call_gemini = fake_call_gemini
agents.critic.call_gemini = fake_call_gemini
agents.tester.call_gemini = fake_call_gemini

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test root endpoint
r = client.get("/")
print("GET / ->", r.status_code, r.json())

# Test full /analyze endpoint with real file upload (multipart/form-data)
with open("../test_data/job_descriptions/JD1_fullstack_developer.txt") as f:
    jd_text = f.read()

with open("../test_data/resumes/01_strong_fullstack_priya.pdf", "rb") as resume_file:
    response = client.post(
        "/analyze",
        data={"job_description": jd_text, "github_username": ""},
        files={"resume": ("priya.pdf", resume_file, "application/pdf")},
    )

print("\nPOST /analyze ->", response.status_code)
import json
result = response.json()
print(json.dumps(result, indent=2))

assert response.status_code == 200, "Expected 200 OK"
assert "final_score" in result, "Missing final_score in response"
assert "recommendation" in result, "Missing recommendation in response"
print("\n✅ Live server end-to-end test PASSED (multipart upload -> full pipeline -> JSON response)")
