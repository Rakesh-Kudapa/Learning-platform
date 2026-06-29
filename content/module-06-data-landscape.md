# Module 6 — Data Landscape

## Eyebrow / kicker
`MODULE 06 • Data Landscape`

## Headline + lead
**Headline:** What the raw material actually *looks* like
**Lead:** Before data becomes evidence, it exists in dozens of shapes and
formats, scattered across systems that were never designed to talk to each
other. This module is a tour of that landscape.

## Narration script
Real-world data doesn't come in one neat package — it comes in many
shapes. Some of it is structured: tidy fields like a diagnosis code or a
lab result, sitting in a table. Some of it is unstructured: a doctor's
free-text notes, a scanned referral letter, words that a computer can't
easily read without help. It also comes in different file formats —
spreadsheets, database tables, modern data-exchange formats like FHIR, and
older hospital messaging formats. And it comes with real problems: missing
values, inconsistent codes, duplicate records, and delays before the data
is even available to look at. Understanding this messiness is the first
step toward fixing it.

## Body sections

### Types of data generated
- **Clinical data** — diagnoses, procedures, lab results, vital signs,
  generated during a patient visit.
- **Administrative / claims data** — what was billed to an insurer, useful
  for tracking utilization and cost, even without clinical detail.
- **Patient-reported data** — surveys, symptom diaries, quality-of-life
  questionnaires filled in by the patient themselves.
- **Device / sensor data** — readings from wearables, glucose monitors, or
  home blood pressure cuffs, generated continuously outside a clinic visit.

### Structured vs. unstructured data
- **Structured data** lives in fixed fields — a lab value, a diagnosis
  code, a date of birth. It's easy for software to search and analyse.
- **Unstructured data** is free text or media — clinical notes, scanned
  PDFs, discharge summaries. It holds rich detail but needs extra
  processing (often natural language processing) before a computer can
  use it.
- In practice, most real-world datasets are a *mix* of both, and a lot of
  the most clinically meaningful detail (the "why" behind a diagnosis)
  often hides in the unstructured notes.

### Common file formats
- **Flat files / CSV** — simple spreadsheets, common for smaller extracts.
- **Relational database tables** — structured data organized into linked
  tables, such as the OMOP Common Data Model (covered in Module 7).
- **FHIR (JSON/XML)** — a modern, API-friendly format for exchanging
  patient data between systems.
- **HL7 v2 messages** — an older but still very common messaging format
  used inside hospitals (e.g. to send a lab result from the lab system to
  the EHR).
- **Free text / scanned documents** — clinical notes and letters, usually
  needing extraction before they're analysis-ready.

### Typical data quality challenges
- **Missingness** — fields that were never filled in, or only captured
  inconsistently across sites.
- **Miscoding** — the wrong diagnosis or procedure code entered, or
  different sites coding the same thing differently.
- **Duplicate records** — the same patient appearing more than once,
  especially across different source systems.
- **Inconsistent units or timestamps** — one site recording weight in
  kilograms, another in pounds; one system's "visit date" meaning
  something subtly different from another's.
- **Lag** — real-world data is often not available immediately; claims
  data in particular can take weeks or months to fully mature.

## Video script (Steve.ai)
- **Suggested context tag:** `messy healthcare data`
- **Suggested style:** animated 2D explainer
- **Scenes:**
  1. Before it becomes evidence, real-world data exists in dozens of
     shapes, scattered across systems that were never built to match.
  2. Some of it is structured — neat fields like a lab result or a
     diagnosis code.
  3. Some of it is unstructured — a doctor's free-text notes, holding rich
     detail a computer can't easily read.
  4. It also comes in different file formats: spreadsheets, database
     tables, modern formats like FHIR, and older hospital messages.
  5. And it comes with real problems — missing values, miscoding,
     duplicates, and delays before it's even ready to use.
  6. Understanding the mess is the first step toward cleaning it up.

## Diagram spec
A 2x2-style visual or simple labelled grid showing the structured/
unstructured split crossed with example sources: top row "Structured" with
icons/labels for lab values, diagnosis codes, billing codes; bottom row
"Unstructured" with icons/labels for clinical notes, scanned letters,
discharge summaries. Use the same rounded-card, brand-gradient-accent style
as other modules' diagrams.

## Callout
**Type:** common-mistake warning
**Text:** Don't assume "more data" automatically means "better evidence."
A huge but messy, inconsistently-coded dataset can be *less* useful than a
smaller, well-curated one — which is exactly why curation (Module 3) and
standards (Module 7) matter so much.

## Knowledge checks

### Question 1
- **Question:** A doctor's free-text clinical notes are an example of:
- **Options:**
  A. Structured data
  B. Unstructured data
  C. Claims data
  D. Device/sensor data
- **Correct answer:** B
- **Explanation:** Free text without a fixed format — like hand-typed
  clinical notes — is unstructured data. It often needs extra processing
  (such as NLP) before it can be analysed alongside structured fields.
- **XP:** 15

### Question 2
- **Question:** A lab result stored in a fixed numeric field is an example
  of:
- **Options:**
  A. Unstructured data
  B. Structured data
  C. A scanned document
  D. A discharge summary
- **Correct answer:** B
- **Explanation:** Structured data lives in fixed fields — like a lab
  value or diagnosis code — making it easy for software to search and
  analyse directly.
- **XP:** 15

### Question 3
- **Question:** Which format is a modern, API-friendly standard for
  exchanging patient data between systems?
- **Options:**
  A. HL7 v2
  B. CSV
  C. FHIR
  D. PDF
- **Correct answer:** C
- **Explanation:** FHIR is the modern, API-based standard built for
  real-time data exchange between systems, unlike older formats like
  HL7 v2 or flat files.
- **XP:** 15

### Question 4
- **Question:** Why can claims data take weeks or months to be fully
  usable?
- **Options:**
  A. It is encrypted permanently
  B. It naturally lags before it's complete and mature
  C. It is always unstructured
  D. It never includes billing codes
- **Correct answer:** B
- **Explanation:** Claims data has an inherent lag — it isn't immediately
  available or complete, which is one of the typical data quality
  challenges covered in this module.
- **XP:** 15

## XP value
60 (4 questions × 15 XP)
