# Module 3 — End-to-End Process

## Eyebrow / kicker
`MODULE 03 • End-to-End Process`

## Headline + lead
**Headline:** From raw records to a *decision*
**Lead:** Real-world data doesn't arrive ready to use. It travels through a
chain of deliberate steps before anyone can trust it enough to act on it.
This module walks that chain, start to finish.

## Narration script
Real-world data starts out messy and scattered. It travels through six
stages before it becomes trustworthy evidence. First we collect it from
many different sources. Then we ingest it into one system. Next we
standardize it so different formats speak the same language. After that we
curate and quality-check it, removing errors and filling gaps where
possible. Then we analyse it to answer a real question. And finally, we turn
that analysis into evidence a decision-maker can actually use. Each step
removes a bit more noise, until what is left is signal.

## Body sections

### The six stages
1. **Collect** — Pull data from its original sources: hospital EHR systems,
   insurance claims databases, patient registries, wearable devices.
2. **Ingest** — Bring that data into one working environment (a data
   warehouse or data lake) so it can all be handled together.
3. **Standardize** — Convert everything into a common structure and
   vocabulary, so "heart attack," "MI," and "myocardial infarction" are
   recognized as the same thing. This is where standards like the OMOP
   Common Data Model or FHIR come in (covered fully in Module 7).
4. **Curate & quality-check** — Find and fix errors, flag missing or
   duplicate records, and document exactly what was changed and why.
5. **Analyse** — Apply statistics or analytics to answer a specific
   question (e.g. "Do patients on Drug A have fewer hospital readmissions
   than patients on Drug B?").
6. **Generate evidence** — Package the analysis into something a regulator,
   payer, or doctor can actually use to make a decision.

### Inputs and outputs at a glance
- **Inputs:** raw, fragmented records in many formats, from many places —
  often incomplete, inconsistently coded, and not designed for research.
- **Outputs:** a clean, well-documented, analysis-ready dataset, and
  ultimately a specific piece of evidence (a report, a published study, a
  safety signal, a submission to a regulator).

### Key activities worth knowing
- **De-duplication** — the same patient may appear in multiple source
  systems; records must be matched and merged correctly.
- **Mapping to standard codes** — translating local hospital codes into a
  shared standard vocabulary.
- **Cohort definition** — precisely specifying which patients belong in
  the study (e.g. "adults diagnosed with Type 2 diabetes after 2018").
- **Documentation** — every cleaning decision is logged, because regulators
  and reviewers need to see exactly how the raw data became the evidence.

## Diagram spec
A left-to-right flow of 6 connected stage boxes, in this order:
`Collect → Ingest → Standardize → Curate & QC → Analyse → Evidence`

Each box should be clickable/hoverable (interactive hotspot) and reveal a
short tooltip with that stage's 1-line description (pull from the "six
stages" list above). Use the same rounded-box, gradient-accent visual style
as the Module 1 lifecycle diagram. The final "Evidence" box should be
visually emphasized (filled with the brand gradient) to show it's the goal
of the whole chain — consistent with the Module 1 funnel diagram's
"EVIDENCE" box.

## Callout
**Type:** Excelra connection
**Text:** This six-stage chain is exactly the kind of work Excelra's data
engineering teams do for clients every day — turning scattered real-world
records into clean, decision-ready datasets.

## Knowledge check
- **Question:** Which step comes right after data is *standardized*?
- **Options:**
  A. Collect
  B. Curate & quality-check
  C. Generate evidence
  D. Ingest
- **Correct answer:** B
- **Explanation:** The order is Collect → Ingest → Standardize → Curate &
  QC → Analyse → Evidence. Standardizing makes the data speak one language;
  curation is the next step, where it gets cleaned and checked before any
  analysis happens.

## XP value
20
