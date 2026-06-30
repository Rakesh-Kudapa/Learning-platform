"""
course_data.py
--------------
Single source of truth that the BACKEND needs to know about the course:

  * MODULE_CONTEXT  -> short grounding text per module, fed to the AI tutor so
                       "Ask a doubt" answers stay accurate and on-topic.
  * TEST_QUESTIONS  -> the whole-course final test. Correct answers live HERE on
                       the server only, so the test is scored server-side and a
                       learner cannot read the answers from the browser.

As you author Modules 3-12 in the front end, extend MODULE_CONTEXT and
TEST_QUESTIONS to match. The structure stays the same.
"""

MODULE_TITLES = [
    "Introduction",
    "Business Overview",
    "End-to-End Process",
    "Key Terminologies",
    "Stakeholders",
    "Data Landscape",
    "Industry Standards",
    "Technology Ecosystem",
    "Current Industry Challenges",
    "Role of Data Engineering & AI",
    "Summary",
    "References",
]

# Grounding context per module id (0-indexed). Keep these factual and concise.
MODULE_CONTEXT = {
    0: ("Introduction to Real-World Data (RWD) and Real-World Evidence (RWE). "
        "RWD is health data collected during everyday care: electronic health "
        "records (EHRs), insurance claims, disease registries, and wearables. "
        "RWE is the clinical evidence about a treatment's use, benefits, or risks "
        "derived by analysing RWD. Memory hook: data is the ingredient, evidence "
        "is the meal. RWE began as a post-approval activity but now spans the "
        "whole life sciences lifecycle, strongest after launch."),
    1: ("Business Overview. The RWE function turns everyday healthcare data into "
        "answers a clinical trial cannot give affordably. Trials are narrow, "
        "expensive, short, and artificial. RWE supports regulatory approvals and "
        "label expansions, proves value to payers (HEOR / market access), detects "
        "rare safety signals, and guides clinical and commercial strategy. "
        "Regulators (FDA, EMA) have formal frameworks for using RWE."),
    2: ("End-to-End Process. Real-world data travels through six stages before "
        "it becomes trustworthy evidence: Collect (pull from EHRs, claims, "
        "registries, wearables), Ingest (into one warehouse or data lake), "
        "Standardize (common structure/vocabulary such as OMOP CDM or FHIR), "
        "Curate & QC (fix errors, flag missing/duplicate records, document "
        "changes), Analyse (statistics to answer a clinical question), and "
        "Generate Evidence (package for a regulator, payer, or clinician). Key "
        "activities include de-duplication, mapping to standard codes, cohort "
        "definition, and documentation of every cleaning decision."),
}

# Whole-course final test. answer = index of the correct option.
# One question per content module (1-11); Module 12 "References" has no quiz.
# Questions are drawn directly from each module's own content/*.md knowledge
# checks so no facts are invented here — see CLAUDE.md "Division of labor".
TEST_QUESTIONS = [
    {"q": "[Module 1] What does RWD stand for?",
     "options": ["Random Wide Data", "Real-World Data", "Regulated Workflow Data", "Reference Width Dataset"],
     "answer": 1},
    {"q": "[Module 1] The simplest way to remember the RWD vs RWE difference is:",
     "options": ["They are identical", "Data is the ingredient; evidence is the meal", "Evidence comes before data", "Both only exist in trials"],
     "answer": 1},
    {"q": "[Module 2] Why does the RWE function exist?",
     "options": ["Trials are cheap and cover everyone", "Regulators banned trials", "Trials are narrow and end at approval, but decisions need evidence on diverse patients over time", "RWD is always cleaner"],
     "answer": 2},
    {"q": "[Module 2] 'HEOR' in the RWE world is mostly about:",
     "options": ["Hospital equipment ordering", "Proving a treatment's value to payers", "Hardware error reporting", "Human embryo organ research"],
     "answer": 1},
    {"q": "[Module 3] Which step comes right after data is standardized?",
     "options": ["Collect", "Curate & quality-check", "Generate evidence", "Ingest"],
     "answer": 1},
    {"q": "[Module 4] Which term describes a hidden factor that affects both the treatment a patient receives and their outcome, potentially distorting results?",
     "options": ["Cohort", "Confounder", "Phenotyping", "Interoperability"],
     "answer": 1},
    {"q": "[Module 5] Which stakeholder primarily decides whether an insurer will pay for a treatment?",
     "options": ["Drug Safety team", "Payers / HTA bodies", "Patients", "Data providers"],
     "answer": 1},
    {"q": "[Module 6] A doctor's free-text clinical notes are an example of:",
     "options": ["Structured data", "Unstructured data", "Claims data", "Device/sensor data"],
     "answer": 1},
    {"q": "[Module 7] Which standard is specifically designed to make sure a lab test means the same thing across different labs and systems?",
     "options": ["OMOP CDM", "FHIR", "LOINC", "21 CFR Part 11"],
     "answer": 2},
    {"q": "[Module 8] Which tool would you use specifically to map a hospital's own database structure onto the OMOP Common Data Model?",
     "options": ["A dashboard / BI tool", "An ETL mapping tool like White Rabbit", "A claims system", "Python"],
     "answer": 1},
    {"q": "[Module 9] Why is 'bias and confounding' a bigger concern in real-world data than in a randomized clinical trial?",
     "options": ["Real-world data is always smaller in size", "Real-world data isn't randomized, so treated and untreated patients can differ systematically for unrelated reasons", "Real-world data is always unstructured", "Regulators ignore real-world data entirely"],
     "answer": 1},
    {"q": "[Module 10] What is the main business value of using AI/automation in this space?",
     "options": ["It removes the need for any human review of evidence", "Faster, more consistent, more scalable evidence generation — with experts still reviewing the output", "It eliminates the need for data standards", "It only helps with patient-reported data"],
     "answer": 1},
    {"q": "[Module 11] Which of these best summarizes why real-world evidence exists as a field?",
     "options": ["To replace clinical trials entirely", "To answer questions trials can't affordably answer — about diverse, real patients, over the long term", "To avoid the need for data standards", "To eliminate the role of regulators"],
     "answer": 1},
]

PASS_MARK = 0.75  # 75% to pass and unlock the certificate

# ------------------------------------------------------------------
# MODULE_QUIZZES — admin-only answer key. Mirrors the `checks` arrays
# wired into COURSE[] in templates/course.html exactly (module ids 0-10;
# Module 12 "References" has no quiz). Used solely by /api/admin/answer-key
# so the admin can see every module's correct answers in one place.
# Never served to non-admin routes.
# ------------------------------------------------------------------
MODULE_QUIZZES = {
    0: [
        {"q": "Which of these is an example of Real-World Data (RWD)?",
         "options": ["The primary result of a tightly controlled randomized clinical trial",
                     "A patient's electronic health record created during routine hospital care",
                     "A chemical structure drawn by a medicinal chemist",
                     "A hypothesis written in a research grant proposal"],
         "answer": 1,
         "explain": "RWD is health data generated during everyday care — EHRs, insurance claims, registries, wearables — not data from a controlled trial or lab bench."},
    ],
    1: [
        {"q": "Why does the Real-World Evidence function exist at all?",
         "options": ["Because clinical trials are cheap and cover every kind of patient",
                     "Because regulators have banned the use of clinical trials",
                     "Because trials are narrow and stop at approval, yet decisions need evidence about diverse real patients over time",
                     "Because real-world data is always cleaner than trial data"],
         "answer": 2,
         "explain": "Trials are controlled, expensive, narrow, and end at approval. RWE answers what happens afterward — in real, diverse populations, over long periods — which trials can't."},
    ],
    2: [
        {"q": "Which step comes right after data is standardized?",
         "options": ["Collect", "Curate & quality-check", "Generate evidence", "Ingest"],
         "answer": 1,
         "explain": "The order is Collect → Ingest → Standardize → Curate & QC → Analyse → Evidence. Standardizing makes the data speak one language; curation is the next step."},
    ],
    3: [
        {"q": "Which of these is an example of Real-World Data (RWD)?",
         "options": ["A randomized controlled trial result", "A patient's electronic health record from routine care", "A drug's chemical formula", "A research grant hypothesis"],
         "answer": 1, "explain": "RWD is data generated during everyday care — like an EHR — not data from a controlled trial or lab bench."},
        {"q": "Which term describes a hidden factor that affects both the treatment a patient receives and their outcome, potentially distorting results?",
         "options": ["Cohort", "Confounder", "Phenotyping", "Interoperability"],
         "answer": 1, "explain": "A confounder is exactly that hidden, distorting factor — it's why real-world studies need careful statistical adjustment, unlike a randomized trial."},
        {"q": "What is the main purpose of the OMOP Common Data Model?",
         "options": ["To replace clinical trials", "To let health data from different sources be organized identically, so studies are comparable", "To generate AI explainer videos", "To collect patient-reported survey data"],
         "answer": 1, "explain": "OMOP CDM defines a standard table structure so data from completely different source systems can be combined and compared."},
        {"q": "\"Phenotyping\" in this field means:",
         "options": ["Sequencing a patient's genome", "Identifying which patients truly have a condition using multiple data signals, not just one code", "Removing personal details from a dataset", "Billing an insurer for a procedure"],
         "answer": 1, "explain": "Phenotyping combines codes, labs, and notes to more reliably identify a condition than trusting a single diagnosis code alone."},
        {"q": "Why is de-identification required before most research use of real-world data?",
         "options": ["To make the data load faster", "To remove or mask personal details so individuals can't be identified", "To convert data into FHIR format", "To increase the sample size"],
         "answer": 1, "explain": "De-identification protects patient privacy by removing or masking identifying details — a requirement before most datasets can be used for research."},
    ],
    4: [
        {"q": "Which stakeholder primarily decides whether an insurer will pay for a treatment?",
         "options": ["Drug Safety team", "Payers / HTA bodies", "Patients", "Data providers"],
         "answer": 1, "explain": "Payers and Health Technology Assessment (HTA) bodies evaluate a treatment's value — often using RWE — to decide coverage and reimbursement."},
        {"q": "Which internal team is primarily responsible for watching real-world data for rare safety signals?",
         "options": ["Drug Safety / Pharmacovigilance", "Market Access", "Commercial / Strategy", "Regulatory Affairs"],
         "answer": 0, "explain": "Drug Safety / Pharmacovigilance teams monitor real-world data specifically to catch safety signals that a smaller trial wouldn't reveal."},
        {"q": "Who are both the original source of the data AND the ultimate intended beneficiary of real-world evidence?",
         "options": ["Regulators", "Payers", "Patients", "Data providers"],
         "answer": 2, "explain": "Patients generate the underlying data through their care, and they're the people every other stakeholder is ultimately trying to help."},
    ],
    5: [
        {"q": "A doctor's free-text clinical notes are an example of:",
         "options": ["Structured data", "Unstructured data", "Claims data", "Device/sensor data"],
         "answer": 1, "explain": "Free text without a fixed format — like hand-typed clinical notes — is unstructured data. It often needs extra processing before it can be analysed."},
        {"q": "A lab result stored in a fixed numeric field is an example of:",
         "options": ["Unstructured data", "Structured data", "A scanned document", "A discharge summary"],
         "answer": 1, "explain": "Structured data lives in fixed fields — like a lab value or diagnosis code — making it easy for software to search and analyse directly."},
        {"q": "Which format is a modern, API-friendly standard for exchanging patient data between systems?",
         "options": ["HL7 v2", "CSV", "FHIR", "PDF"],
         "answer": 2, "explain": "FHIR is the modern, API-based standard built for real-time data exchange between systems, unlike older formats like HL7 v2 or flat files."},
        {"q": "Why can claims data take weeks or months to be fully usable?",
         "options": ["It is encrypted permanently", "It naturally lags before it's complete and mature", "It is always unstructured", "It never includes billing codes"],
         "answer": 1, "explain": "Claims data has an inherent lag — it isn't immediately available or complete, which is one of the typical data quality challenges."},
    ],
    6: [
        {"q": "Which standard is specifically designed to make sure a lab test means the same thing across different labs and systems?",
         "options": ["OMOP CDM", "FHIR", "LOINC", "21 CFR Part 11"],
         "answer": 2, "explain": "LOINC is the standard naming system specifically for laboratory tests and measurements. OMOP standardizes data structure; FHIR standardizes exchange."},
        {"q": "What does the OMOP Common Data Model primarily solve?",
         "options": ["It gives data a common table structure so multi-source studies are possible", "It generates AI explainer videos", "It replaces the need for clinical trials", "It encrypts patient records"],
         "answer": 0, "explain": "OMOP CDM lets health data from different source systems be organized identically, making large multi-source studies comparable."},
        {"q": "Which regulation sets requirements for electronic records and signatures to ensure a regulatory submission's data trail is trustworthy?",
         "options": ["ICD-10", "21 CFR Part 11", "SNOMED CT", "HL7 v2"],
         "answer": 1, "explain": "21 CFR Part 11 is a US FDA regulation specifically about the security and attributability of electronic records and signatures."},
        {"q": "How does SNOMED CT differ from ICD-10?",
         "options": ["SNOMED CT is only used for billing", "SNOMED CT is a much more detailed clinical vocabulary than ICD-10", "ICD-10 is newer than SNOMED CT", "They are exactly the same thing"],
         "answer": 1, "explain": "SNOMED CT captures much finer clinical detail (findings, procedures, symptoms) than ICD-10, which is mainly used for diagnosis coding and billing."},
    ],
    7: [
        {"q": "Which tool would you use specifically to map a hospital's own database structure onto the OMOP Common Data Model?",
         "options": ["A dashboard / BI tool", "An ETL mapping tool like White Rabbit", "A claims system", "Python"],
         "answer": 1, "explain": "ETL mapping tools like White Rabbit are built specifically to help map a source system's unique structure onto a standard model like OMOP."},
        {"q": "Where is clinical data first generated, before any processing happens?",
         "options": ["In a dashboard", "In source systems like EHRs and claims platforms", "In OHDSI ATLAS", "In a Python script"],
         "answer": 1, "explain": "Source systems (EHRs, claims platforms) are where data is first created, during actual patient care or billing."},
        {"q": "Which tools are used specifically to process very large healthcare datasets efficiently?",
         "options": ["Spark / Databricks", "OHDSI ATLAS only", "A single Excel spreadsheet", "LOINC"],
         "answer": 0, "explain": "Spark and Databricks are big-data processing tools built to handle very large datasets efficiently."},
    ],
    8: [
        {"q": "Why is \"bias and confounding\" a bigger concern in real-world data than in a randomized clinical trial?",
         "options": ["Real-world data is always smaller in size", "Real-world data isn't randomized, so treated and untreated patients can differ systematically for unrelated reasons", "Real-world data is always unstructured", "Regulators ignore real-world data entirely"],
         "answer": 1, "explain": "Randomization in a trial spreads differences between patients evenly across groups. Real-world data has no such randomization."},
        {"q": "Which laws specifically restrict how health data can be shared, stored, and re-used?",
         "options": ["HIPAA (US) and GDPR (EU)", "ICD-10 and SNOMED CT", "OMOP and FHIR", "21 CFR Part 11 only"],
         "answer": 0, "explain": "HIPAA and GDPR are privacy laws that govern how health data can be shared and used."},
        {"q": "Two hospitals both claim to be \"FHIR-compliant,\" but their underlying data still doesn't line up perfectly. This illustrates which challenge?",
         "options": ["Scale", "Interoperability", "Regulatory acceptance", "Bias"],
         "answer": 1, "explain": "Even with shared standards in place, real systems can still implement them inconsistently — that gap is an interoperability challenge."},
        {"q": "What does the \"scale\" challenge in real-world evidence mainly refer to?",
         "options": ["The need for serious infrastructure to process huge data volumes", "The need for more clinical trials", "A lack of clinical vocabulary standards", "Patient privacy concerns"],
         "answer": 0, "explain": "Modern healthcare generates enormous data volumes — processing it requires real infrastructure, or even well-designed studies become impractical."},
    ],
    9: [
        {"q": "What is the main business value of using AI/automation in this space?",
         "options": ["It removes the need for any human review of evidence", "Faster, more consistent, more scalable evidence generation — with experts still reviewing the output", "It eliminates the need for data standards", "It only helps with patient-reported data"],
         "answer": 1, "explain": "AI and automation speed up and scale the work — but human experts still review and finalize outputs."},
        {"q": "What role does NLP (natural language processing) play in this space?",
         "options": ["It extracts structured information from free-text clinical notes", "It replaces the need for data warehouses", "It only generates videos", "It is a privacy regulation"],
         "answer": 0, "explain": "NLP unlocks previously unusable unstructured data — like clinical notes — by pulling structured information out of free text."},
        {"q": "Why is ML-based phenotyping considered more reliable than relying on a single diagnosis code?",
         "options": ["It ignores lab results entirely", "It combines many signals (codes, labs, notes) instead of trusting one code that could be missing or wrong", "It only works with structured data", "It replaces the need for any clinical review"],
         "answer": 1, "explain": "A single code can be missing or miscoded. ML phenotyping combines multiple signals for a more reliable picture of who truly has a condition."},
        {"q": "What is distinctive about \"agentic\" AI systems, as described in this module?",
         "options": ["They can carry out multi-step workflows with less manual intervention", "They only translate text between languages", "They replace the need for any data standards", "They are limited to generating images"],
         "answer": 0, "explain": "Agentic AI systems coordinate multi-step tasks — like pulling data, analysing it, and drafting a summary — with far less manual handling than before."},
    ],
    10: [
        {"q": "Which of these best summarizes why real-world evidence exists as a field?",
         "options": ["To replace clinical trials entirely", "To answer questions trials can't affordably answer — about diverse, real patients, over the long term", "To avoid the need for data standards", "To eliminate the role of regulators"],
         "answer": 1, "explain": "RWE doesn't replace trials — it fills the gaps trials structurally can't: narrow populations, high cost, short follow-up, and artificial conditions."},
        {"q": "Complete the memory hook from this course: \"Data is the ingredient, evidence is the ___.\"",
         "options": ["Meal", "Standard", "Pipeline", "Regulation"],
         "answer": 0, "explain": "Data is the raw ingredient, and evidence is what you get after carefully analysing it — the meal."},
        {"q": "In the six-stage process from Module 3, which stage comes first?",
         "options": ["Analyse", "Collect", "Curate & quality-check", "Generate evidence"],
         "answer": 1, "explain": "The process starts with Collect (gathering data from sources like EHRs and claims), before it's ingested, standardized, curated, analysed, and turned into evidence."},
    ],
}
