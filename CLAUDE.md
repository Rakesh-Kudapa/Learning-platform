# CLAUDE.md — project memory for Claude Code

**Project:** Excelra RWD/RWE interactive learning platform (Flask + SQLite + vanilla-JS course).

## Read first
**`ARCHITECTURE.md` is the single source of truth.** Read it fully before writing any
code. It defines the data model, every API contract, the front-end design, the course
content model, and the branch-by-branch build order.

## How to work
- **One feature = one branch** off `main`, in the order in ARCHITECTURE.md §12.
  Next up: `feat/course-progress`.
- Each branch is done when it has: endpoint(s) + front-end wiring + a short smoke test
  + an ARCHITECTURE/README note. Then it can be merged to `main`.
- The DB is **schema-first**: all 7 tables already exist in `models.py`. Do **not**
  add migrations — just write endpoints against the existing models.

## Conventions
- Backend: Flask **application factory** in `app.py`; auth is a blueprint (`auth.py`);
  models + Flask-Login plumbing live in `models.py`.
- AI doubt tutor: call `llm.ask_tutor()` (`llm.py`). Provider/key come from `.env`
  (`LLM_PROVIDER` = gemini|groq|ollama). **Never expose the key to the browser.**
- Front end: the course is **one self-contained file** `templates/course.html`
  (vanilla HTML/CSS/JS, no framework). All UI derives from the `state` object.
  Add a thin `fetch` bridge for new `/api/*` calls; treat HTTP 401 as "go to /".
- Keep `course_data.py` (`MODULE_TITLES`, `MODULE_CONTEXT`, `TEST_QUESTIONS`) in sync
  with the `COURSE[]` array in `course.html` as modules are authored.

## Hard rules
- **Final-test answers never go to the client.** Score server-side; `PASS_MARK = 0.70`.
- Passwords stay hashed (Werkzeug). All `/api/*` and `/course` require login.
- Validate/clamp all inputs; use SQLAlchemy (no raw SQL strings).

## Run
```
pip install -r requirements.txt
cp .env.example .env        # add a free GEMINI_API_KEY for the tutor
python app.py               # http://localhost:5000
```
