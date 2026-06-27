# ARCHITECTURE — Excelra RWD/RWE Interactive Learning Platform

> **Purpose of this document.** This is the build blueprint. It describes the
> complete target architecture of the tool so it can be developed feature-by-feature
> (one git branch per feature). The scaffold and `feat/auth` branch already exist and
> are tested — everything marked **BUILT** is done; everything marked **PLANNED**
> is to be implemented on the named branch. Build in the order given in §12.

---

## 1. Product Overview

An AI-powered, gamified, single-topic e-learning course delivered as a small
full-stack web app. Topic: **Real-World Data (RWD) & Real-World Evidence (RWE)**
in life sciences. It is built for the *Excelra Life Sciences Learning Repository –
Fresher Edition* and must let a learner with **no prior knowledge** complete the
course in **~1 hour**.

Beyond a static course, the tool is a real product: accounts, a database, a
per-module AI doubt tutor, a pre/post knowledge self-assessment, a server-scored
final test that unlocks a certificate, feedback capture, and a crowdsourced
"learner contributions" module where knowledge added by past learners is shown to
future ones.

**Design goals**
- Beginner-first: concept-level, visual, narrated. No tutorials/code dumps.
- Self-contained front end (no SPA framework) so it is easy to host and grade.
- Schema-first DB so feature branches add endpoints, never migrations.
- Free/low-cost stack throughout (SQLite, free LLM tier).

---

## 2. Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| Backend | **Python 3.11+ / Flask** (application-factory pattern) | `app.py` factory |
| ORM / DB | **Flask-SQLAlchemy + SQLite** | swap `SQLALCHEMY_DATABASE_URI` to Postgres later, no model changes |
| Auth | **Flask-Login** + Werkzeug password hashing | session cookies |
| AI tutor | **Free LLM via `requests`** — Gemini (default) / Groq / Ollama | `llm.py`, provider chosen in `.env` |
| Narration | **Web Speech API** (browser `speechSynthesis`) | zero-dependency baseline; ElevenLabs hero VO added for submission |
| Front end | **Vanilla HTML/CSS/JS**, single self-contained file | `templates/course.html` |
| Config | **python-dotenv** | `.env` (gitignored), `.env.example` committed |

No build step, no node toolchain. The course front end is one HTML file served by Flask.

---

## 3. High-Level Architecture

```
                    ┌──────────────────────────────────────────┐
                    │              Browser (learner)            │
                    │  login.html   course.html (SPA-like)      │
                    │  - render loop + state object             │
                    │  - gamification engine (xp/badges/levels) │
                    │  - Web Speech narration                   │
                    └───────────────┬──────────────────────────┘
                                    │  HTTPS (session cookie)
                                    │  JSON over fetch()
                    ┌───────────────▼──────────────────────────┐
                    │            Flask app (app.py)             │
                    │  auth blueprint │ course + /api/* routes  │
                    │  Flask-Login (sessions)                   │
                    └───────┬───────────────────────┬──────────┘
                            │                        │
                ┌───────────▼─────────┐   ┌──────────▼───────────┐
                │  SQLite (course.db) │   │  Free LLM provider   │
                │  via SQLAlchemy     │   │  Gemini/Groq/Ollama  │
                │  7 tables           │   │  (llm.py, requests)  │
                └─────────────────────┘   └──────────────────────┘
```

---

## 4. Project Structure

```
rwd_rwe_project/
├── app.py                 # BUILT  application factory: config, db, login, routes
├── models.py              # BUILT  SQLAlchemy models (7) + Flask-Login plumbing
├── auth.py                # BUILT  auth blueprint: /register /login /logout
├── llm.py                 # BUILT  free-LLM wrapper for the doubt tutor
├── course_data.py         # BUILT  server-side module context + final-test answers
├── requirements.txt       # BUILT
├── .env.example           # BUILT  SECRET_KEY + LLM provider config
├── .gitignore             # BUILT  ignores .env, instance/, __pycache__
├── README.md              # BUILT  run + git workflow
├── ARCHITECTURE.md        # this file
├── .vscode/launch.json    # BUILT  F5 = run Flask
├── instance/
│   └── course.db          # (gitignored) created at runtime
└── templates/
    ├── login.html         # BUILT  sign in / register (matches brand)
    ├── index.html         # BUILT  status landing (dev only)
    └── course.html        # BUILT (modules 1–2 + engine; 3–12 to author)
```

---

## 5. Data Model (SQLite via SQLAlchemy)

All seven tables already exist in `models.py`. Endpoints are added per branch.

**users**
| col | type | notes |
|---|---|---|
| id | int PK | |
| name | str(80) | |
| email | str(120) unique, indexed | login id |
| password_hash | str(255) | Werkzeug hash; never store raw |
| created_at | datetime | |
| methods | `set_password()`, `check_password()` | |

**progress** — one row per user
| col | type | notes |
|---|---|---|
| id | int PK | |
| user_id | FK users, unique | |
| data | text (JSON) | `{xp, done, checks, badges, current}` |
| updated_at | datetime | |

**knowledge_ratings** — pre & post self-assessment
| col | type | notes |
|---|---|---|
| id | int PK | |
| user_id | FK users | |
| stage | str | `'pre'` \| `'post'` |
| level | str | `'beginner'` \| `'medium'` \| `'advanced'` |
| created_at | datetime | enables before→after growth view |

**doubts** — AI tutor Q&A log
| col | type | notes |
|---|---|---|
| id | int PK | |
| user_id | FK users | |
| module_id | int | which module asked from |
| question | text | |
| answer | text | |
| created_at | datetime | |

**test_results** — whole-course final test
| col | type | notes |
|---|---|---|
| id | int PK | |
| user_id | FK users | |
| score / total | int | |
| passed | bool | gate for certificate |
| created_at | datetime | |

**feedback** — end-of-course UX + change requests
| col | type | notes |
|---|---|---|
| id | int PK | |
| user_id | FK users | |
| rating | int | 1–5 |
| experience | text | "how did you find it?" |
| suggestions | text | "changes we should make" |
| created_at | datetime | |

**contributions** — crowdsourced extra knowledge
| col | type | notes |
|---|---|---|
| id | int PK | |
| user_id | FK users | |
| title | str(140) | |
| content | text | |
| status | str | `'approved'` (default) \| `'pending'` (optional moderation) |
| created_at | datetime | surfaced in the Learner Contributions module |

---

## 6. Backend API Contract

All `/api/*` and `/course` routes require an authenticated session (Flask-Login).
Unauthenticated requests to protected routes redirect to `/login` (HTML) or should
return `401` (for `fetch`). Front end treats `401` as "go to /login".

### Auth & shell — **BUILT** (`feat/auth`)
| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/` | — | 302 → `/course` if authed else `/login` |
| GET/POST | `/login` | `email,password` | page / 302 → `/course` |
| POST | `/register` | `name,email,password` | 302 → `/course` |
| GET | `/logout` | — | 302 → `/login` |
| GET | `/course` | — | serves `course.html` |
| GET | `/api/me` | — | `{name,email}` |
| GET | `/health` | — | `{status:"ok"}` |

### Progress — **PLANNED** (`feat/course-progress`)
| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/progress` | — | saved state JSON (or `{}`) |
| POST | `/api/progress` | full state JSON | `{ok:true}` |

### Assessment — **BUILT** (`feat/pre-post-feedback-knowledge`)
| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/assessment` | — | `{pre:{level,at}|null, post:{level,at}|null}` |
| POST | `/api/assessment` | `{stage:'pre'|'post', level}` | `{ok:true}` |

### AI doubt tutor — **PLANNED** (`feat/ask-doubt-tutor`)
| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/api/ask` | `{module_id:int, question:str}` | `{answer:str}` |

Server builds the prompt from `course_data.MODULE_CONTEXT[module_id]`, calls
`llm.ask_tutor()`, logs to `doubts`, returns the answer. Never expose the API key
to the client. Rate-limit lightly (e.g. per-user cooldown) to protect the free tier.

### Final test & certificate — **PLANNED** (`feat/final-test-certificate`)
| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/test` | — | `[{id,q,options[]}]` — **answers stripped** |
| POST | `/api/test/submit` | `{answers:{qid:optionIndex}}` | `{score,total,passed}` |
| GET | `/certificate` | — | rendered certificate if `passed` else 302 back |

**Scoring is server-side only** (answers live in `course_data.TEST_QUESTIONS`,
`PASS_MARK = 0.70`). The browser never receives correct answers. Certificate is
stamped with `current_user.name`, date, and score; printable / downloadable.

### Feedback — **BUILT** (`feat/pre-post-feedback-knowledge`)
| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/api/feedback` | `{rating, experience, suggestions}` | `{ok:true}` |

### Community knowledge — **BUILT** (`feat/pre-post-feedback-knowledge`)
| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/contributions` | — | approved `[{author_name,title,content,created_at}]` |
| POST | `/api/contributions` | `{title, content}` | `{ok:true}` (status defaults `approved`) |

---

## 7. Front-End Architecture (`course.html`)

A single file: `<style>` (design tokens) + markup shell + one `<script>`. No framework.

**State object** (hydrated from `/api/progress`, mirrored to a local cache):
```js
state = {
  name, xp,
  done:   { [moduleId]: true },   // completed modules
  checks: { [moduleId]: bool },   // knowledge-check pass/fail
  badges: [ ...keys ],
  current: int,                   // active module index
}
```

**Render loop.** `render()` reads `state.current`, renders that module's `body()`,
rebuilds the sidebar nav (`renderNav`), updates the HUD + waveform (`renderHUD`),
and persists. All UI derives from `state` — single source of truth.

**Module data** (`COURSE[]`):
```js
{ id, title, short,
  type: 'content' | 'locked' | 'special',
  body: () => htmlString,
  check: { q, opts:[...], answer:int, xp:int, explain } }
```

**Backend bridge.** A thin layer wraps `fetch` for `/api/me`, `/api/progress`,
`/api/ask`, `/api/assessment`, `/api/test`, `/api/feedback`, `/api/contributions`.
On `401` → `location.href = '/'`. Progress writes are debounced.

**Views the front end must implement**
- `login.html` (separate page) — BUILT
- Course shell + Modules 1–12 — Modules 1–2 BUILT, 3–12 to author
- Pre-assessment screen (gate before Module 1) — `feat/pre-post-assessment`
- Per-module **Ask-a-doubt** panel — `feat/ask-doubt-tutor`
- Final assessment screen — `feat/final-test-certificate`
- Certificate view — `feat/final-test-certificate`
- Post-course screen: post-assessment + feedback + "add your knowledge" — `feat/feedback-ux` + `feat/community-knowledge`
- Module 13 **Learner Contributions** (renders `/api/contributions`) — `feat/community-knowledge`

---

## 8. Gamification Spec

| Element | Rule |
|---|---|
| **XP** | +20 for a knowledge check correct on first try; +10 if wrong/retried; +per-question on final test |
| **Levels** | 1 per module (12). Current level = completed modules + 1 |
| **Unlock gating** | Module *n* locks until module *n-1*'s check is passed |
| **Progress** | % complete drives the header **waveform** (noise→signal) — also the progress bar |
| **Badges** | `First Steps` (M1 done) · `Data Detective` (2 checks) · `Halfway Hero` (reach M6) · `Standards Savvy` (M7 done) · `Evidence Expert` (all modules) · `Certified` (pass test) · `Perfect Run` (100% test) |
| **Toasts** | XP/level/badge events animate a bottom toast |

**Interactive element types to build across modules** (mandatory variety):
knowledge-check MCQ (every module) · flash cards (M4 terminology) · drag-and-drop
(M6 file-format↔data-type; M3 order-the-workflow) · interactive hotspots (M3
workflow diagram) · click-to-reveal · decision-based branching scenario · one timed
quiz round · 12-question final assessment.

---

## 9. Course Content Model (RWD/RWE)

12 mandatory modules (from the assignment) + a 13th crowdsourced module. Each content
module = intro prose + original SVG diagram(s) + knowledge check + doubt panel +
narration text.

| # | Module | Topic-correct content focus |
|---|---|---|
| 1 | Introduction | RWD vs RWE, why it matters, **position in the life sciences lifecycle** (lifecycle map) |
| 2 | Business Overview | what/why the RWE function exists; objectives; Excelra relevance |
| 3 | End-to-End Process | data sources → ingest → standardize → curate/QC → analyze → evidence (hotspot workflow) |
| 4 | Key Terminologies | 18–20 flash cards (RWD, RWE, EHR, claims, registry, OMOP, FHIR, cohort, HEOR, confounding, external control arm, etc.) |
| 5 | Stakeholders | pharma (RWE/HEOR/medical/safety/regulatory), payers, regulators, providers, data vendors, patients; **consumers of outputs** |
| 6 | Data Landscape | EHR/claims/registry/wearable; structured vs unstructured; formats (CSV, OMOP tables, FHIR/JSON); quality challenges |
| 7 | Industry Standards | OMOP CDM, FHIR, HL7, ICD-10/SNOMED/LOINC, FDA RWE framework, 21 CFR Part 11 — and **why** each matters |
| 8 | Technology Ecosystem | EHR systems, data warehouses, OHDSI/ATLAS, cloud, Spark/Databricks, R/Python analytics; how they interact |
| 9 | Current Challenges | data quality/missingness, interoperability, privacy (HIPAA/GDPR), bias/confounding, regulatory acceptance, scale |
| 10 | Role of Data Engineering & AI | ETL→CDM, NLP on notes, ML phenotyping, GenAI synthesis, agentic automation — **business value**, not implementation |
| 11 | Summary | key takeaways, recap, further reading |
| 12 | References | citations for standards, repositories, AI/media assets |
| 13 | **Learner Contributions** | renders approved `contributions` — extra knowledge from past learners |

`course_data.py` holds `MODULE_TITLES`, `MODULE_CONTEXT` (LLM grounding per module),
`TEST_QUESTIONS` (12, answers server-side), `PASS_MARK`. **Extend these as Modules
3–12 are authored.**

---

## 10. User Journey / Course Flow

```
register/login
   └─> PRE-assessment (beginner|medium|advanced)         [knowledge_ratings: pre]
        └─> Module 1 … 12  (sequential unlock)
             • each: read + diagram + knowledge check + Ask-a-doubt (AI)
        └─> Module 13: Learner Contributions (read)
        └─> FINAL TEST (unlocks after all modules) ──server-scored──┐
             • pass (≥70%) ─> CERTIFICATE (name + date + score)     │
        └─> POST-assessment (how I grew)                 [knowledge_ratings: post]
        └─> FEEDBACK (rating + experience + suggestions) [feedback]
        └─> "Add knowledge we missed?" ─> CONTRIBUTION   [contributions → Module 13]
```

---

## 11. Configuration (`.env`)

```
SECRET_KEY=<long random>
LLM_PROVIDER=gemini            # gemini | groq | ollama
GEMINI_API_KEY=<free key>      # https://aistudio.google.com/app/apikey
GEMINI_MODEL=gemini-2.0-flash
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

---

## 12. Git Branch Strategy / Build Order

One feature = one branch off `main`; merge when green. Content authoring runs in parallel.

1. `feat/auth` — login/register/logout, course behind login wall ............. **BUILT ✅**
2. `feat/course-progress` — `/api/progress`; front end loads/saves state to DB
3. `feat/pre-post-feedback-knowledge` — pre/post knowledge gate + growth view; end-of-course feedback; crowdsourced contributions + Learner Contributions page ... **BUILT ✅**
4. `feat/ask-doubt-tutor` — per-module doubt panel; `/api/ask` → `llm.py`; logs to `doubts`
5. `feat/final-test-certificate` — `/api/test`, `/api/test/submit` (server-scored), `/certificate`
6. `content/modules-3-12` — author remaining modules + interactions (parallel)

**Definition of done per branch:** endpoint(s) + front-end wiring + a short smoke
test + README/ARCHITECTURE note updated.

---

## 13. Security & Integrity Notes

- Passwords hashed (Werkzeug); never logged or returned.
- **Final-test answers never sent to the client**; scoring is server-side.
- All `/api/*` require an authenticated session; validate/clamp all inputs.
- LLM key stays server-side; cap question length and add a per-user cooldown.
- Contributions default `approved`; flip to `pending` + an admin view if moderation is wanted before public display.
- Use parameterized ORM queries (SQLAlchemy) — no raw SQL string building.

---

## 14. Setup & Run

```bash
cd rwd_rwe_project
python -m venv .venv && source .venv/bin/activate     # Win: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # add a free GEMINI_API_KEY for the tutor
python app.py                                         # http://localhost:5000
```
VS Code: press **F5** → "Flask: run course backend".

---

## 15. Mapping to the Excelra Assignment

| Requirement | Where it lives |
|---|---|
| 12 mandatory modules | §9 Modules 1–12 |
| Position in lifecycle | Module 1 (lifecycle map) |
| Stakeholders | Module 5 |
| 15–20 terminologies | Module 4 flash cards |
| Interactive navigation, knowledge checks | Front-end engine (§7–8) |
| ≥10-question final assessment | §6 final test (12 Q) |
| AI narration | Web Speech (+ ElevenLabs hero VO) |
| Original diagrams/infographics | SVG, generated in `course.html` |
| Gamification (badges, points, levels, progress, scenarios…) | §8 |
| Completion certificate | §6 `/certificate` |
| Progress tracking | `progress` table + waveform |
| AI usage | content/quiz/diagram/narration via Claude; tutor via free LLM |
| Deliverables: course + facilitator guide + quick-reference + AI-usage summary | course (this app) + 3 companion docs (authored separately) |

---

*End of architecture. Build branch-by-branch per §12; keep `course_data.py` and the
`COURSE[]` array in `course.html` in sync as modules are authored.*
