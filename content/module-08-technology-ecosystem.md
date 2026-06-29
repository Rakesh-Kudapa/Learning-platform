# Module 8 — Technology Ecosystem

## Eyebrow / kicker
`MODULE 08 • Technology Ecosystem`

## Headline + lead
**Headline:** The *machinery* behind the process
**Lead:** Every stage of the journey from Module 3 runs on real technology.
This module names the tools and shows how they hand work off to each other.

## Narration script
Every stage of the real-world data journey runs on actual technology. Data
starts inside source systems — electronic health records and claims
systems — which feed into a data warehouse or data lake, often hosted on
a cloud platform. From there, large-scale tools like Spark or Databricks
process huge volumes efficiently. Specialized tools like the OHDSI
community's ATLAS help map messy source data onto standard structures
like OMOP. Once the data is standardized, analysts use languages like
Python, R, and SQL to actually study it. And the results usually surface
through dashboards or reports that a non-technical stakeholder can read.
None of these tools work alone — each one hands its output to the next.

## Body sections

### Source systems
- **EHR systems** (e.g. Epic, Cerner) — where clinical data is first
  generated, during patient care.
- **Claims systems** — insurer platforms where billing data originates.

### Data infrastructure
- **Data warehouses / data lakes** — large storage systems that hold data
  from multiple sources so it can be processed together. A warehouse
  usually holds cleaned, structured data; a lake can hold raw and
  unstructured data too.
- **Cloud platforms** (AWS, Azure, Google Cloud) — where most modern data
  infrastructure is hosted, offering scalable storage and compute.
- **Spark / Databricks** — big-data processing tools that handle very
  large datasets efficiently, especially useful when combining data from
  many sources at once.

### Standardization tooling
- **OHDSI ATLAS** — a tool from the OHDSI open-science community for
  exploring and querying data already mapped to the OMOP Common Data
  Model.
- **ETL mapping tools** (e.g. White Rabbit, Rabbit-in-a-Hat) — help map a
  source database's unique structure onto a standard model like OMOP.

### Analytics & reporting
- **Python / R** — the most common languages for statistical analysis of
  real-world data (e.g. survival analysis, regression modelling).
- **SQL** — used to query structured data directly out of databases and
  data warehouses.
- **Dashboards / BI tools** — turn analysis results into visual reports
  that non-technical stakeholders (payers, executives, clinicians) can
  actually read and use.

### How it all connects
Source systems → ingestion into a warehouse/lake (often cloud-hosted) →
large-scale processing (Spark/Databricks) → standardization onto a common
model (OMOP, via tools like ATLAS) → analysis (Python/R/SQL) → reporting
and dashboards. Each tool exists to move the data one step closer to being
trustworthy evidence.

## Video script (Steve.ai)
- **Suggested context tag:** `data technology pipeline`
- **Suggested style:** animated 2D explainer
- **Scenes:**
  1. Every stage of the real-world data journey runs on real technology.
  2. It starts in source systems — electronic health records and claims
     platforms — where the data is first created.
  3. That data flows into a cloud-hosted data warehouse or lake, where
     large-scale tools like Spark or Databricks process it efficiently.
  4. Specialized tools help map it onto standard structures, so it's
     comparable across sources.
  5. Then analysts use Python, R, and SQL to actually study it.
  6. And the results show up in dashboards anyone can read. One pipeline,
     each tool handing off to the next.

## Diagram spec
A left-to-right pipeline diagram with 5 connected boxes: `Source systems
(EHR/Claims)` → `Cloud data warehouse/lake` → `Big-data processing
(Spark/Databricks)` → `Standardization (OMOP/ATLAS)` → `Analytics &
dashboards (Python/R/SQL/BI)`. Same visual style as the Module 3 workflow
diagram — interactive hotspots with a one-line tooltip per box.

## Callout
**Type:** Excelra connection
**Text:** This is the exact stack Excelra's data engineering teams work in
daily — cloud platforms, Spark/Databricks-scale processing, and
standardization tooling — to turn raw client data into analysis-ready
datasets.

## Knowledge checks

### Question 1
- **Question:** Which tool would you use specifically to map a hospital's
  own database structure onto the OMOP Common Data Model?
- **Options:**
  A. A dashboard / BI tool
  B. An ETL mapping tool like White Rabbit
  C. A claims system
  D. Python
- **Correct answer:** B
- **Explanation:** ETL mapping tools like White Rabbit are built
  specifically to help map a source system's unique structure onto a
  standard model like OMOP. Dashboards visualize results, claims systems
  generate raw data, and Python is used for analysis after standardization.
- **XP:** 15

### Question 2
- **Question:** Where is clinical data first generated, before any
  processing happens?
- **Options:**
  A. In a dashboard
  B. In source systems like EHRs and claims platforms
  C. In OHDSI ATLAS
  D. In a Python script
- **Correct answer:** B
- **Explanation:** Source systems (EHRs, claims platforms) are where data
  is first created, during actual patient care or billing — everything
  else in the pipeline processes it afterward.
- **XP:** 15

### Question 3
- **Question:** Which tools are used specifically to process very large
  healthcare datasets efficiently?
- **Options:**
  A. Spark / Databricks
  B. OHDSI ATLAS only
  C. A single Excel spreadsheet
  D. LOINC
- **Correct answer:** A
- **Explanation:** Spark and Databricks are big-data processing tools
  built to handle very large datasets efficiently, especially when
  combining data from many sources.
- **XP:** 15

## XP value
45 (3 questions × 15 XP)
