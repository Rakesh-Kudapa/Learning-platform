# Module 4 — Key Terminologies

> **Module type note:** this module's primary visual IS the flashcard grid
> (per ARCHITECTURE.md §8 gamification spec: "flash cards (M4 terminology)").
> No separate workflow diagram is needed — implement each term below as a
> flip-card: front shows the term, back shows the definition.

## Eyebrow / kicker
`MODULE 04 • Key Terminologies`

## Headline + lead
**Headline:** The *vocabulary* of real-world evidence
**Lead:** Every field has its own shorthand. Knowing these 20 terms means
you can read any RWD/RWE document, conversation, or job posting and
actually follow what's being said.

## Narration script
You don't need to memorize a textbook to work with real-world data — you
just need to recognise about twenty recurring words. Flip through these
cards at your own pace. Each one is something you'll see again and again:
in data sources, in standards, in the people who do this work. By the end
of this module, the alphabet soup of RWD and RWE will start to make sense.

## Body sections

### Why terminology matters first
Before standards, processes, or technology make sense, the *words* need to
make sense. These 20 terms are the building blocks for every other module
in this course — flip through them now, and the rest gets easier.

## Flashcard terms (20)

1. **RWD (Real-World Data)** — Health data collected during everyday care,
   outside of a controlled clinical trial (e.g. EHRs, claims, registries).
2. **RWE (Real-World Evidence)** — The clinical conclusions about a
   treatment's use, benefits, or risks, drawn from analysing RWD.
3. **EHR (Electronic Health Record)** — A digital version of a patient's
   medical chart, maintained by a healthcare provider over time.
4. **Claims data** — Records created when a provider bills an insurer for
   care; useful for tracking diagnoses, procedures, and costs.
5. **Registry** — An organized system that tracks patients with a specific
   condition, exposure, or procedure, often over many years.
6. **Cohort** — A defined group of patients who share a common
   characteristic (e.g. the same diagnosis or treatment) and are studied
   together.
7. **OMOP CDM (Common Data Model)** — A standard database structure that
   lets health data from many different sources be stored the same way, so
   it can be analysed consistently.
8. **FHIR (Fast Healthcare Interoperability Resources)** — A modern
   standard for exchanging patient data between different health IT
   systems.
9. **HL7** — A family of international standards for exchanging clinical
   and administrative health data between systems (FHIR is its newest one).
10. **ICD-10** — The standard coding system used worldwide to record
    diagnoses (e.g. a specific code for "Type 2 diabetes").
11. **SNOMED CT** — A detailed clinical vocabulary used to record findings,
    symptoms, and procedures inside electronic health records.
12. **LOINC** — A standard naming system for laboratory tests and clinical
    measurements, so "blood glucose" means the same thing everywhere.
13. **Structured data** — Information stored in a fixed, organized format,
    like a spreadsheet column (e.g. a lab value, a diagnosis code).
14. **Unstructured data** — Free-text information without a fixed format,
    like a doctor's hand-typed clinical notes.
15. **External control arm** — A comparison group built from real-world
    data, used in place of (or alongside) a placebo group in a trial.
16. **HEOR (Health Economics & Outcomes Research)** — The discipline that
    measures a treatment's cost, value, and real-world outcomes, mainly to
    inform what payers will cover.
17. **Confounder** — A hidden factor that affects both the treatment a
    patient receives and their outcome, which can distort results if not
    accounted for.
18. **Interoperability** — The ability of different health IT systems to
    exchange data and correctly understand what it means.
19. **Data warehouse** — A large storage system that holds cleaned,
    structured data from multiple sources, ready for analysis (compare to
    a "data lake," which holds raw/unstructured data).
20. **Phenotyping** — Using available data (codes, labs, notes) to
    accurately identify which patients truly have a specific condition.

## Video script (Steve.ai)
- **Suggested context tag:** `healthcare data`
- **Suggested style:** animated 2D explainer
- **Scenes:**
  1. Every industry has its own shorthand — and real-world evidence is no
     different.
  2. RWD is the raw data: think electronic health records, insurance
     claims, and patient registries.
  3. RWE is what you get after analysing that data — real conclusions
     about how a treatment performs.
  4. Standards like FHIR, HL7, and OMOP make sure data from different
     hospitals can actually talk to each other.
  5. And terms like cohort, confounder, and phenotyping describe how
     researchers study that data carefully and fairly.
  6. Twenty terms, one shared language. Flip through the cards — you've
     got this.

## Callout
**Type:** memory hook
**Text:** Group them as you go: **sources** (EHR, claims, registry),
**standards** (FHIR, HL7, ICD-10, SNOMED, LOINC, OMOP), and **method words**
(cohort, confounder, phenotyping, external control arm). Three buckets, not
twenty random words.

## Knowledge checks

### Question 1
- **Question:** Which of these is an example of Real-World Data (RWD)?
- **Options:**
  A. A randomized controlled trial result
  B. A patient's electronic health record from routine care
  C. A drug's chemical formula
  D. A research grant hypothesis
- **Correct answer:** B
- **Explanation:** RWD is data generated during everyday care — like an
  EHR — not data from a controlled trial or lab bench.
- **XP:** 15

### Question 2
- **Question:** Which term describes a hidden factor that affects both the
  treatment a patient receives *and* their outcome, potentially distorting
  results?
- **Options:**
  A. Cohort
  B. Confounder
  C. Phenotyping
  D. Interoperability
- **Correct answer:** B
- **Explanation:** A confounder is exactly that hidden, distorting factor —
  it's why real-world studies need careful statistical adjustment, unlike a
  randomized trial where treatment assignment is controlled.
- **XP:** 15

### Question 3
- **Question:** What is the main purpose of the OMOP Common Data Model?
- **Options:**
  A. To replace clinical trials
  B. To let health data from different sources be organized identically,
     so studies are comparable
  C. To generate AI explainer videos
  D. To collect patient-reported survey data
- **Correct answer:** B
- **Explanation:** OMOP CDM defines a standard table structure so data
  from completely different source systems can be combined and compared.
- **XP:** 15

### Question 4
- **Question:** "Phenotyping" in this field means:
- **Options:**
  A. Sequencing a patient's genome
  B. Identifying which patients truly have a condition using multiple
     data signals, not just one code
  C. Removing personal details from a dataset
  D. Billing an insurer for a procedure
- **Correct answer:** B
- **Explanation:** Phenotyping combines codes, labs, and notes to more
  reliably identify a condition than trusting a single diagnosis code
  alone.
- **XP:** 15

### Question 5
- **Question:** Why is de-identification required before most research
  use of real-world data?
- **Options:**
  A. To make the data load faster
  B. To remove or mask personal details so individuals can't be identified
  C. To convert data into FHIR format
  D. To increase the sample size
- **Correct answer:** B
- **Explanation:** De-identification protects patient privacy by removing
  or masking identifying details — a requirement before most datasets can
  be used for research.
- **XP:** 15

## XP value
75 (5 questions × 15 XP)
