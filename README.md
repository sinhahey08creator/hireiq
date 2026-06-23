<<<<<<< HEAD
# HireIQ — Autonomous Multi-Agent Hiring Assistant

Recruiter uploads a Job Description + Candidate Resume (PDF) + optional GitHub username.
4 AI agents (each = one Gemini prompt) analyze the candidate and produce a final hiring score.

```
Upload  ->  Planner  ->  Researcher  ->  Critic  ->  Tester  ->  Final Score
```

---

## 🚀 Setup — Step by Step

### 1. Get a free Gemini API key
Go to https://aistudio.google.com/app/apikey and create a free API key.

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Now open .env and paste your Gemini API key
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

You should see: `HireIQ API is running` at http://localhost:8000

### 3. Frontend Setup

Open a **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

Open the URL it gives you (usually http://localhost:5173).

---

## 🧪 How to Test

1. Open the frontend in your browser.
2. Paste a Job Description (e.g. "Looking for a Full Stack Developer skilled in React, Node.js, MongoDB, Git").
3. Upload any resume PDF.
4. (Optional) Enter a real GitHub username.
5. Click **"Analyze Candidate"**.
6. Wait ~10-20 seconds — you'll see all 4 agent outputs + a final score.

---

## 📁 Project Structure

```
hireiq/
├── backend/
│   ├── main.py              # FastAPI app, /analyze endpoint, pipeline orchestration
│   ├── gemini_client.py      # Shared Gemini API caller
│   ├── agents/
│   │   ├── planner.py        # Extracts skills + weights from JD
│   │   ├── researcher.py      # Matches resume against required skills
│   │   ├── critic.py          # Finds red flags
│   │   └── tester.py          # Generates interview questions
│   ├── utils/
│   │   ├── pdf_parser.py      # Extracts text from resume PDF
│   │   ├── github_fetch.py    # Fetches GitHub public activity
│   │   └── json_helper.py     # Safely parses Gemini's JSON output
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js              # Calls the backend /analyze endpoint
    │   ├── index.css
    │   └── components/
    │       ├── UploadForm.jsx       # Screen 1
    │       └── ResultsDashboard.jsx # Screens 2-6
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## ⚠️ Common Issues

| Problem | Fix |
|---|---|
| `GEMINI_API_KEY not found` | Make sure you created `.env` (not just `.env.example`) inside `backend/` |
| CORS error in browser | Make sure backend is running on port 8000 — check `API_BASE` in `frontend/src/api.js` |
| Gemini returns weird JSON | `json_helper.py` has a fallback — but you may need to tweak prompts slightly for edge cases |
| GitHub rate limit error | GitHub's public API allows 60 requests/hour without auth — fine for demo, but don't spam it |

---

## 🎯 Next Steps (after MVP works)

- Test with 5-10 different resumes + JDs (Member 3's job — collect these!)
- Polish UI — add loading spinners, color-coded score bars
- Add error handling for malformed PDFs
- Prepare your 3-minute demo script using 1-2 best sample resumes
=======
# hireiq
HireIQ — Autonomous Multi-Agent AI Hiring Assistant. 4 AI agents (Planner, Researcher, Critic, Tester) collaboratively evaluate candidates against a job description and generate a final hiring score. Built with FastAPI, React, and Google Gemini API.
>>>>>>> db96356c826f9886401fae746a258a9180618073
