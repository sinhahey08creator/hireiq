# HireIQ — Test Data Guide

Use these combinations to test your 4 agents. Each pair is designed to produce a
**different, predictable kind of result** — so you can verify the agents are actually
working correctly (not just returning random output).

---

## 📂 Files

```
test_data/
├── job_descriptions/
│   ├── JD1_fullstack_developer.txt
│   ├── JD2_data_analyst.txt
│   ├── JD3_backend_developer.txt
│   ├── JD4_frontend_developer.txt
│   └── JD5_devops_engineer.txt
└── resumes/
    ├── 01_strong_fullstack_priya.pdf
    ├── 02_weak_redflags_rahul.pdf
    ├── 03_strong_dataanalyst_ananya.pdf
    ├── 04_mismatch_backend_sara.pdf
    ├── 05_strong_frontend_karan.pdf
    └── 06_average_devops_vikram.pdf
```

---

## 🧪 Recommended Test Cases

### Test 1 — The "Happy Path" (use this for your live demo!)
| | |
|---|---|
| JD | `JD1_fullstack_developer.txt` |
| Resume | `01_strong_fullstack_priya.pdf` |
| GitHub username | `priya-codes` *(fictional — won't be found, that's OK, see note below)* |

**Expected result:** High match score (80-95%), few/no red flags, relevant React/Node
interview questions. **This is your best demo candidate — strong, clean, no surprises.**

---

### Test 2 — Red Flags Should Trigger
| | |
|---|---|
| JD | `JD1_fullstack_developer.txt` |
| Resume | `02_weak_redflags_rahul.pdf` |

**Expected result:** Lower match score, and Critic Agent **should** flag things like:
- Keyword stuffing (lists ML, Blockchain, AWS — totally unrelated to a fresh grad intern role)
- Vague project descriptions ("many features", "modern tech stack" — no specifics)
- No deployed links or real GitHub repo names mentioned

**If Critic Agent doesn't catch this, your prompt needs tuning — this is your test case for it.**

---

### Test 3 — Clean Strong Match, Different Domain
| | |
|---|---|
| JD | `JD2_data_analyst.txt` |
| Resume | `03_strong_dataanalyst_ananya.pdf` |

**Expected result:** High match (85%+), no red flags. Confirms agents generalize beyond
just "full stack" roles.

---

### Test 4 — Skill Mismatch (Researcher should catch this)
| | |
|---|---|
| JD | `JD3_backend_developer.txt` *(wants Python, Django, PostgreSQL, Docker)* |
| Resume | `04_mismatch_backend_sara.pdf` *(is actually a Frontend dev — React, CSS, Figma)* |

**Expected result:** LOW match score (~20-35%). Researcher's "missing" list should include
Python, Django, PostgreSQL, Docker. This proves the matching logic isn't just "any tech
keyword = pass."

---

### Test 5 — Strong Match, Different Role
| | |
|---|---|
| JD | `JD4_frontend_developer.txt` |
| Resume | `05_strong_frontend_karan.pdf` |

**Expected result:** High match (80%+), clean — good second demo candidate if you want
to show two different roles in your pitch.

---

### Test 6 — Average Candidate, Partial Gaps
| | |
|---|---|
| JD | `JD5_devops_engineer.txt` *(wants Kubernetes, full AWS, CI/CD)* |
| Resume | `06_average_devops_vikram.pdf` *(has Docker, basic AWS, GitHub Actions — but admits "limited Kubernetes exposure")* |

**Expected result:** Medium match score (50-65%). Tests that the system can express
nuance, not just pass/fail.

---

## ⚠️ Note on GitHub Usernames

The `github.com/...` usernames written inside the resumes (e.g. `priya-codes`) are
**fictional** — they won't resolve on the real GitHub API. Two options:

1. **For demo purposes:** Leave the GitHub username field blank — the pipeline still
   works fine using only resume text (Researcher/Critic just skip GitHub analysis).
2. **For testing the GitHub Critic logic specifically:** Use a real public username
   like `octocat` (GitHub's official test account) to confirm `github_fetch.py` works.

---

## ✅ How to Use This for Your Demo Script

**Recommended 3-minute demo flow:**
1. Show **Test 1** (strong candidate) — fast, clean, impressive result. This is your "wow" moment.
2. Show **Test 2** (red flags) — proves the Critic Agent isn't just decoration, it
   genuinely catches something a busy recruiter might miss.
3. Mention Test 3-6 exist as evidence you tested broadly (don't need to demo live,
   just have screenshots ready as backup).
