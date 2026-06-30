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
