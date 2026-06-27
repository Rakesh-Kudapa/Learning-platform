# CLAUDE.md — project memory for Claude Code

**Project:** Excelra RWD/RWE interactive learning platform (Flask + SQLite + vanilla-JS course).

## Current status (read this first)
On `main`, two branches are merged and tested:
- `feat/auth` — login/register/logout, course behind a login wall
- `feat/pre-post-feedback-knowledge` — pre/post knowledge-level gate,
  end-of-course feedback form, and crowdsourced "contributions" (extra
  learner knowledge), with a Learner Contributions page

**Next up, in order:** `feat/ask-doubt-tutor` → `feat/final-test-certificate`
→ `feat/course-progress`. See ARCHITECTURE.md §12 for the full plan.

Only **Modules 1 and 2** have real lesson content written (in `mod1()`/`mod2()`
inside `templates/course.html`). Modules 3–12 are placeholder "locked" stubs.
**Do not write lesson content yourself** — see the section below.

## Division of labor — read carefully
This project has two separate workstreams that must stay separate:
- **Engineering (Claude Code's job):** routes, database, JS, git, tests,
  debugging, new features. Everything in ARCHITECTURE.md §6–§8.
- **Subject-matter content (NOT Claude Code's job):** the actual RWD/RWE
  teaching content for Modules 3–12. This is authored by the project owner
  with Claude (the chat assistant) as research/writing help, reviewed for
  accuracy, then dropped into `content/*.md` files using `content/TEMPLATE.md`.

**When a `content/module-0X-*.md` file appears in the repo, your job is purely
mechanical:** read it, then add a `modN()` function to `templates/course.html`
following the exact pattern of `mod1()`/`mod2()` (same CSS classes, same
`checkBlock()`/`pageNav()` helpers, same callout/diagram structure), wire it
into the `COURSE[]` array (flip its `type` from `'locked'` to `'content'`),
build the SVG diagram from the file's "Diagram spec" section, and add the
matching entry to `MODULE_TITLES`/`MODULE_CONTEXT` in `course_data.py`.
**Do not invent, change, or "improve" any facts, numbers, or definitions from
the content file.** If something in the content file seems ambiguous for
implementation (e.g. diagram layout), make a reasonable formatting choice but
never alter the substance — flag it instead.

## How to work
- **One feature = one branch** off `main`, in the order in ARCHITECTURE.md §12.
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

## Suggested first prompt to give Claude Code
> "Read CLAUDE.md and ARCHITECTURE.md fully, and look at the current git log
> and branches. Confirm you understand the division of labor (you do
> engineering; module content comes pre-written in `content/*.md` files).
> Then: (1) implement `content/module-03-end-to-end-process.md` into
> `templates/course.html` and `course_data.py` exactly as described in the
> 'Division of labor' section above, on a new branch `content/module-03`,
> with a smoke test, then merge it. (2) After that, start
> `feat/ask-doubt-tutor` per ARCHITECTURE.md §6."

