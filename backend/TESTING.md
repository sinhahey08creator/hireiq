# Testing Without a Real Gemini API Key

Two test scripts are included so you can verify the backend code is correct
**before** plugging in a real Gemini API key (useful for whoever doesn't have
a key yet, or wants to confirm nothing crashes before burning API quota).

They work by faking ("mocking") Gemini's responses with a simple keyword-matching
function — so they test your **code's logic**, not the AI's actual judgment quality.

## 1. `test_pipeline_mock.py` — tests the agents directly

Runs all 6 sample resume/JD combos from `test_data/` straight through
Planner -> Researcher -> Critic -> Tester -> Final Score, without going through
the web server.

```bash
cd backend
python test_pipeline_mock.py
```

Expected output: all 6 test cases print their results and end with
`✅ ALL 6 TEST CASES RAN WITHOUT CRASHING.`

## 2. `test_server_live.py` — tests the actual FastAPI server + file upload

Spins up the real FastAPI app in-process and sends a real HTTP multipart
request to `/analyze` with an actual PDF file — exactly how the React
frontend will call it.

```bash
cd backend
python test_server_live.py
```

Expected output: `200 OK` responses and a full JSON result printed, ending
with `✅ Live server end-to-end test PASSED`.

## Once you have a real GEMINI_API_KEY

1. Copy `.env.example` to `.env` and add your key.
2. Run the real server: `uvicorn main:app --reload --port 8000`
3. Test through the actual React frontend, or with `curl`:

```bash
curl -X POST http://localhost:8000/analyze \
  -F "job_description=$(cat ../test_data/job_descriptions/JD1_fullstack_developer.txt)" \
  -F "github_username=" \
  -F "resume=@../test_data/resumes/01_strong_fullstack_priya.pdf"
```

If real Gemini output looks weird or doesn't match expectations in
`test_data/TEST_GUIDE.md`, the issue is in **prompt wording**
(edit the prompts in `backend/agents/*.py`), not in the surrounding code —
since the mock tests already proved the plumbing works.

## ⚠️ Important Fix Already Applied

The original `google-generativeai` Python package is **deprecated**. This
project uses the new official `google-genai` SDK instead (see `gemini_client.py`).
Do not downgrade or switch back — the deprecated package may stop working
entirely at any time.
