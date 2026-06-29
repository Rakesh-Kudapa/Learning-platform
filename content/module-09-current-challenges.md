# Module 9 — Current Industry Challenges

## Eyebrow / kicker
`MODULE 09 • Current Industry Challenges`

## Headline + lead
**Headline:** What still makes this *hard*
**Lead:** None of the previous modules are solved problems — they're
ongoing challenges that every team in this field works against, every day.

## Narration script
Even with good standards and good technology, real-world evidence work is
genuinely hard. Data quality and missing information are constant
problems — no source system was built purely for research. Different
systems still don't always talk to each other smoothly, even with
standards in place. Privacy rules rightly limit what can be shared and
how. Because real-world data isn't randomized like a clinical trial,
hidden bias and confounding can quietly distort results if you're not
careful. Regulators don't accept every use of real-world evidence equally
yet — trust is still being built. And the sheer scale of modern healthcare
data requires serious infrastructure just to process it at all. These
challenges are exactly why this field needs careful, skilled people, not
just bigger datasets.

## Body sections

### Data quality & missingness
Source systems were built to support care and billing, not research —
so fields go unfilled, get miscoded, or arrive late. Cleaning and
validating data (Module 3) is a constant, ongoing effort, not a one-time
fix.

### Interoperability
Even with standards like FHIR and OMOP, real systems still vary in how
consistently they're implemented. Two hospitals both claiming to be
"FHIR-compliant" may still structure details differently underneath.

### Privacy & compliance
Laws like HIPAA (US) and GDPR (EU) protect patient privacy and restrict how
health data can be shared, stored, and re-used. De-identification (Module
4) is required before most research use, and getting it right — without
destroying the data's research value — is a real skill.

### Bias & confounding
Clinical trials randomize patients to remove bias. Real-world data never
does — patients who receive a treatment differ systematically from those
who don't, for reasons that have nothing to do with the treatment itself.
Without careful statistical handling, those differences can masquerade as
treatment effects.

### Regulatory acceptance
Regulators have made real progress (the FDA's RWE Framework, Module 7),
but acceptance still varies by use case — RWE is more readily accepted for
some questions (like long-term safety) than others (like proving a new
drug works as well as a randomized trial would show).

### Scale
Modern healthcare generates enormous volumes of data. Processing it
requires real infrastructure (Module 8) — without it, even well-designed
studies become impractical.

## Video script (Steve.ai)
- **Suggested context tag:** `data challenges`
- **Suggested style:** animated 2D explainer
- **Scenes:**
  1. Good standards and good technology don't make this easy — real-world
     evidence work still runs into hard, ongoing challenges.
  2. Data quality and missing information are constant problems, because
     no source system was built purely for research.
  3. Privacy rules rightly limit what can be shared, and systems still
     don't always talk to each other smoothly.
  4. Because real-world data isn't randomized like a trial, hidden bias
     can quietly distort results if you're not careful.
  5. Regulators don't accept every use of real-world evidence equally yet
     — and the sheer scale of healthcare data takes real infrastructure to
     process.
  6. These challenges are exactly why this field needs skilled people, not
     just bigger datasets.

## Diagram spec
A simple hexagon or honeycomb of 6 connected challenge cards, evenly
weighted (no hierarchy implied): Data Quality & Missingness ·
Interoperability · Privacy & Compliance · Bias & Confounding · Regulatory
Acceptance · Scale. Each card click-to-reveals its 1-line description from
the body sections above.

## Callout
**Type:** common-mistake warning
**Text:** A frequent beginner mistake is assuming a bigger dataset
automatically means stronger evidence. Scale without quality control just
means the same problems (missingness, bias, miscoding) at a larger size.

## Knowledge checks

### Question 1
- **Question:** Why is "bias and confounding" a bigger concern in
  real-world data than in a randomized clinical trial?
- **Options:**
  A. Real-world data is always smaller in size
  B. Real-world data isn't randomized, so treated and untreated patients
     can differ systematically for unrelated reasons
  C. Real-world data is always unstructured
  D. Regulators ignore real-world data entirely
- **Correct answer:** B
- **Explanation:** Randomization in a trial spreads differences between
  patients evenly across groups. Real-world data has no such randomization,
  so who receives a treatment and who doesn't can correlate with other
  factors that affect the outcome — creating confounding if not carefully
  handled.
- **XP:** 15

### Question 2
- **Question:** Which laws specifically restrict how health data can be
  shared, stored, and re-used?
- **Options:**
  A. HIPAA (US) and GDPR (EU)
  B. ICD-10 and SNOMED CT
  C. OMOP and FHIR
  D. 21 CFR Part 11 only
- **Correct answer:** A
- **Explanation:** HIPAA and GDPR are privacy laws that govern how health
  data can be shared and used — separate from the clinical vocabulary or
  data-structure standards covered in Module 7.
- **XP:** 15

### Question 3
- **Question:** Two hospitals both claim to be "FHIR-compliant," but their
  underlying data still doesn't line up perfectly. This illustrates which
  challenge?
- **Options:**
  A. Scale
  B. Interoperability
  C. Regulatory acceptance
  D. Bias
- **Correct answer:** B
- **Explanation:** Even with shared standards in place, real systems can
  still implement them inconsistently — that gap is an interoperability
  challenge.
- **XP:** 15

### Question 4
- **Question:** What does the "scale" challenge in real-world evidence
  mainly refer to?
- **Options:**
  A. The need for serious infrastructure to process huge data volumes
  B. The need for more clinical trials
  C. A lack of clinical vocabulary standards
  D. Patient privacy concerns
- **Correct answer:** A
- **Explanation:** Modern healthcare generates enormous data volumes —
  processing it requires real infrastructure, or even well-designed
  studies become impractical.
- **XP:** 15

## XP value
60 (4 questions × 15 XP)
