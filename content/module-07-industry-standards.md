# Module 7 — Industry Standards

## Eyebrow / kicker
`MODULE 07 • Industry Standards`

## Headline + lead
**Headline:** The common *language* that makes any of this possible
**Lead:** Without shared standards, data from one hospital can't be
compared to data from another. This module covers the standards that let
real-world data from anywhere become evidence that's actually trustworthy.

## Narration script
Imagine two hospitals each describe a heart attack a different way — one
types it as free text, the other uses an old internal code. Without a
shared language, you can't combine their data at all. That's exactly what
standards solve. OMOP gives data a common table structure. FHIR and HL7
let systems exchange patient information using a shared format. ICD-10,
SNOMED, and LOINC make sure a diagnosis, a clinical finding, or a lab test
means exactly the same thing everywhere it's recorded. And on the
regulatory side, the FDA's real-world evidence framework and rules like 21
CFR Part 11 set out how trustworthy that data needs to be before it can
support a real decision. Standards aren't paperwork — they're what makes
comparison possible at all.

## Body sections

### Data structure standards
- **OMOP CDM (Common Data Model)** — defines a standard set of tables so
  health data from completely different source systems can be organized
  identically, making large multi-source studies possible. Maintained by
  the OHDSI (Observational Health Data Sciences and Informatics)
  community.
- **FHIR (Fast Healthcare Interoperability Resources)** — a modern,
  API-based standard for exchanging health data between systems in
  real time, widely adopted by current EHR platforms.
- **HL7 v2** — an older, message-based standard still heavily used inside
  hospitals for things like sending a lab result from the lab system to
  the patient's chart. FHIR is HL7's newer, more flexible successor.

### Clinical vocabulary standards
- **ICD-10** — the standard coding system for diagnoses, used worldwide
  for billing and epidemiology.
- **SNOMED CT** — a much more detailed clinical vocabulary, capturing fine
  distinctions in symptoms, findings, and procedures beyond what ICD-10
  can.
- **LOINC** — the standard naming system for laboratory tests and
  measurements, so "fasting blood glucose" means exactly the same thing
  whichever lab generated it.

### Regulatory standards
- **FDA RWE Framework** — formal guidance describing when and how the FDA
  will consider real-world evidence in regulatory decisions, including
  supporting new indications or post-marketing safety requirements.
- **21 CFR Part 11** — a US FDA regulation setting requirements for
  electronic records and signatures, ensuring the data trail behind a
  regulatory submission is secure, attributable, and trustworthy.

### Why each one matters
Every standard here solves the same underlying problem: making data
*comparable* and *trustworthy* across different sources, systems, and
time periods. Without them, RWE would only ever describe one hospital, one
system, one moment — never the broader real-world picture decision-makers
actually need.

## Video script (Steve.ai)
- **Suggested context tag:** `data standards healthcare`
- **Suggested style:** animated 2D explainer
- **Scenes:**
  1. Two hospitals describe the same heart attack two completely different
     ways. Without a shared language, their data can't be compared at all.
  2. That's what standards solve. OMOP gives data a common structure, so
     studies from many sources can be combined.
  3. FHIR and HL7 let different systems exchange patient data using a
     shared format.
  4. ICD-10, SNOMED, and LOINC make sure a diagnosis or a lab test means
     exactly the same thing everywhere.
  5. And regulatory rules like the FDA's RWE framework and 21 CFR Part 11
     set out how trustworthy that data needs to be before it can support
     a real decision.
  6. Standards aren't paperwork — they're what makes comparison possible.

## Diagram spec
Two grouped columns: left column "Data structure & exchange" listing OMOP
CDM, FHIR, HL7 as stacked labelled boxes; middle column "Clinical
vocabulary" listing ICD-10, SNOMED CT, LOINC; right column "Regulatory"
listing FDA RWE Framework, 21 CFR Part 11. A connecting line/arrow beneath
all three columns labelled "→ comparable, trustworthy evidence" to show
they all feed the same outcome.

## Callout
**Type:** Excelra connection
**Text:** Mapping messy source data onto standards like OMOP and FHIR —
and making sure that mapping is documented and defensible — is core, daily
work for data curation teams like Excelra's.

## Knowledge checks

### Question 1
- **Question:** Which standard is specifically designed to make sure a lab
  test (like "fasting blood glucose") means the same thing across
  different labs and systems?
- **Options:**
  A. OMOP CDM
  B. FHIR
  C. LOINC
  D. 21 CFR Part 11
- **Correct answer:** C
- **Explanation:** LOINC is the standard naming system specifically for
  laboratory tests and measurements. OMOP standardizes overall data
  structure, FHIR standardizes data exchange, and 21 CFR Part 11 is a
  regulatory record-keeping rule — not a vocabulary standard.
- **XP:** 15

### Question 2
- **Question:** What does the OMOP Common Data Model primarily solve?
- **Options:**
  A. It gives data a common table structure so multi-source studies are
     possible
  B. It generates AI explainer videos
  C. It replaces the need for clinical trials
  D. It encrypts patient records
- **Correct answer:** A
- **Explanation:** OMOP CDM lets health data from different source systems
  be organized identically, making large multi-source studies comparable.
- **XP:** 15

### Question 3
- **Question:** Which regulation sets requirements for electronic records
  and signatures to ensure a regulatory submission's data trail is
  trustworthy?
- **Options:**
  A. ICD-10
  B. 21 CFR Part 11
  C. SNOMED CT
  D. HL7 v2
- **Correct answer:** B
- **Explanation:** 21 CFR Part 11 is a US FDA regulation specifically
  about the security and attributability of electronic records and
  signatures.
- **XP:** 15

### Question 4
- **Question:** How does SNOMED CT differ from ICD-10?
- **Options:**
  A. SNOMED CT is only used for billing
  B. SNOMED CT is a much more detailed clinical vocabulary than ICD-10
  C. ICD-10 is newer than SNOMED CT
  D. They are exactly the same thing
- **Correct answer:** B
- **Explanation:** SNOMED CT captures much finer clinical detail (findings,
  procedures, symptoms) than ICD-10, which is mainly used for diagnosis
  coding and billing.
- **XP:** 15

## XP value
60 (4 questions × 15 XP)
