# Excelra — RWD/RWE Interactive Course Platform

A full-stack learning platform for the **Real-World Data & Real-World Evidence**
course: a Flask backend + SQLite database serving an interactive, gamified
e-learning front end with accounts, an AI doubt-tutor, a final test, certificate
generation, and a community knowledge module.

> **Status:** Step 1 — scaffold. Backend boots, DB models defined. Features are
> layered on per branch (see roadmap below).

---

## What it does (target)

- **Accounts & login** — learners sign up, log in, and resume where they left off.
- **Pre-course self-assessment** — Beginner / Medium / Advanced, captured up front.
- **12-module interactive course** — gamified: XP, badges, levels, progress.
- **Ask a doubt (AI tutor)** — per-module Q&A powered by a free LLM, grounded on
  that module's content.
- **Whole-course final test** — scored on the server; passing unlocks the cert.
- **Certificate** — generated with the learner's real details after passing.
- **Post-course reflection** — re-rate knowledge (to show growth) + experience +
  feedback + suggested changes.
- **Learners' Extra Knowledge** — learners contribute tips not in the course;
  these are stored and auto-surfaced in a dedicated module for future learners.

---

## Project structure

```
rwd_rwe_project/
├── app.py             # Flask app factory + routes
├── models.py          # SQLAlchemy schema (all tables)
├── course_data.py     # module context for the tutor + final-test questions
├── templates/         # Jinja templates (index, login, course, certificate…)
├── instance/          # SQLite db lives here (git-ignored)
├── requirements.txt
├── .env.example       # copy to .env and fill in
└── .vscode/launch.json
```

---

## Run it locally (VS Code)

1. **Open the folder in VS Code.** Install the *Python* + *Pylance* extensions if prompted.
2. **Create a virtual environment** and select it as the interpreter:
   ```bash
   python -m venv .venv
   # macOS/Linux:
   source .venv/bin/activate
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   ```
   In VS Code: `Ctrl/Cmd+Shift+P` → *Python: Select Interpreter* → pick `.venv`.
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your env file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env`: set a `SECRET_KEY`, and add a free LLM key (see below).
5. **Run** — press `F5` (uses `.vscode/launch.json`) or:
   ```bash
   flask --app app run --debug
   ```
6. Open **http://127.0.0.1:5000** — you should see the "Backend running" page.

---

## Free LLM for the doubt-tutor

Pick **one** provider in `.env` (`LLM_PROVIDER=`) and add its key:

| Provider | Cost | Get a key |
|---|---|---|
| `gemini` *(default)* | Free tier | https://aistudio.google.com/app/apikey |
| `groq` | Free | https://console.groq.com/keys |
| `ollama` | Free, fully local — no key | https://ollama.com |

The tutor integration arrives on the `feat/ai-doubts` branch (Step 5).

---

## Git workflow

We build one feature per branch and merge to `main` via pull request.

```bash
# one-time, if not already a repo
git init
git add .
git commit -m "Step 1: project scaffold + data model"
git branch -M main

# add your remote and push
git remote add origin <your-repo-url>
git push -u origin main

# start the next slice
git checkout -b feat/auth
# …work…
git add . && git commit -m "feat: auth (login/register/sessions)"
git push -u origin feat/auth   # open a PR into main
```

### Branch roadmap

| Step | Branch | Adds |
|---|---|---|
| 1 | `feat/scaffold` | repo, config, models, runnable app |
| 2 | `feat/auth` | login / register / sessions |
| 3 | `feat/course-frontend` | serve course + progress sync |
| 4 | `feat/pre-post-assessment` | knowledge level before & after |
| 5 | `feat/ai-doubts` | per-module AI doubt tutor |
| 6 | `feat/final-test-cert` | whole-course test → certificate |
| 7 | `feat/feedback` | end-of-course experience + feedback |
| 8 | `feat/contributions` | Learners' Extra Knowledge module |
| — | `feat/content-3-12` | author Modules 3–12 |

---

*Excelra — Proprietary & Confidential.*
