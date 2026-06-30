# CLAUDE.md — project memory for Claude Code

**Project:** Excelra RWD/RWE interactive learning platform (Flask + SQLite + vanilla-JS course).

## Current status (read this first)
On `main`:
- `feat/auth` — login/register/logout, course behind a login wall
- `feat/pre-post-feedback-knowledge` — pre/post knowledge-level gate,
  end-of-course feedback form, and crowdsourced "contributions" (extra
  learner knowledge), with a Learner Contributions page
- `feat/ask-doubt-tutor` — per-module AI doubt panel
- `feat/explainer-videos` — per-module video player, videos uploaded for
  Modules 1–11 (Module 12 is references-only, no video)
- `feat/admin-dashboard` — `/admin` (gated by `ADMIN_EMAIL`), `APP_MODE`
  env var (`user`|`admin`|`full`) for two separate deploy targets
- `feat/final-test-certificate` — `/api/test`, `/api/test/submit`,
  `/api/test/results` (server-scored, `PASS_MARK = 0.75`), in-app
  Performance Dashboard + printable certificate
- `feat/admin-controls` — full answer key (`/api/admin/answer-key`),
  multi-admin grant/revoke (`AdminGrant` table, `/api/admin/admins*`,
  super-admin-only), per-user per-module unlock overrides (`ModuleUnlock`
  table, `/api/admin/unlock|lock|unlock-all|lock-all`) that bypass the
  sequential gate, and universal admin access to `/course` with every
  module pre-unlocked for the admin's own account
- `feat/admin-user-management` — server-side progress sync (`/api/progress`,
  written by `course.html` on every `persist()`, debounced) so the admin
  can see real per-module knowledge-check scores; per-user performance
  report (`/api/admin/users/<id>/report`) with CSV download; edit
  name/email (`PATCH /api/admin/users/<id>`); delete a single user or
  bulk-delete via checkboxes (`DELETE` / `/api/admin/users/bulk-delete`),
  both blocked for the primary admin and for deleting yourself

**All 12 modules now have real lesson content** (`mod1()`–`mod12()` in
`templates/course.html`), each with multi-question knowledge checks except
Module 12 (References — citation list only, no quiz, auto-marked complete
on visit). The whole-course final exam (13 questions, one per content
module) is in `course_data.TEST_QUESTIONS`.

**Next up:** `feat/course-progress` (server-persisted progress beyond
localStorage). See ARCHITECTURE.md §12.

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
- **Final-test answers never go to the client.** Score server-side; `PASS_MARK = 0.75`.
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

## Pending feature: explainer videos (`feat/explainer-videos`)
Each module's narration bar (the `narrateBar()` function in `course.html` —
the pill with the 🔊 Listen button) needs a second action added alongside it:
**▶ Watch video**.

- **Video files:** static mp4s placed at `static/videos/module-0X.mp4`
  (2-digit zero-padded module number, e.g. `module-04.mp4`). Create the
  `static/videos/` folder; Flask serves it automatically at `/static/videos/...`.
- **UI:** extend `narrateBar()` so it renders the existing Listen button
  plus a "▶ Watch video" button in the same pill row. Clicking Watch toggles
  an inline `<video controls>` element directly below the bar (rounded
  corners, full width, matching the existing `.diagram` card style).
- **Graceful fallback:** most modules won't have a video yet. Don't hard-fail
  if the file is missing — either check existence server-side (a small
  `/api/has-video/<n>` check, or simplest: just attempt to load it and use
  the `<video>` element's `onerror` to hide the Watch button) so an absent
  video never breaks the page.
- **Source of each video's script:** the matching `content/module-0X-*.md`
  file's "Video script (Steve.ai)" section.
- This satisfies the assignment's "AI-generated explainer video" requirement,
  alongside the existing Web Speech narration.