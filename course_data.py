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
    "Current Challenges",
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
}

# Whole-course final test. answer = index of the correct option.
# NOTE: starter set covering RWD/RWE fundamentals; finalise as content is built.
TEST_QUESTIONS = [
    {"q": "What does RWD stand for?",
     "options": ["Random Wide Data", "Real-World Data", "Regulated Workflow Data", "Reference Width Dataset"],
     "answer": 1},
    {"q": "What does RWE stand for?",
     "options": ["Real-World Evidence", "Routine Workflow Engine", "Regulatory Working Estimate", "Random Effect Weighting"],
     "answer": 0},
    {"q": "Which is an example of Real-World Data?",
     "options": ["A randomized controlled trial result", "A patient's EHR from routine care", "A drug's chemical formula", "A grant proposal hypothesis"],
     "answer": 1},
    {"q": "The simplest way to remember the RWD vs RWE difference is:",
     "options": ["They are identical", "Data is the ingredient; evidence is the meal", "Evidence comes before data", "Both only exist in trials"],
     "answer": 1},
    {"q": "Why does the RWE function exist?",
     "options": ["Trials are cheap and cover everyone", "Regulators banned trials", "Trials are narrow and end at approval, but decisions need evidence on diverse patients over time", "RWD is always cleaner"],
     "answer": 2},
    {"q": "Historically, RWE was used mainly in which lifecycle stage?",
     "options": ["Discovery", "Preclinical", "Post-approval (after a drug reaches the market)", "Target identification"],
     "answer": 2},
    {"q": "Which is a common SOURCE of real-world data?",
     "options": ["Insurance claims data", "A periodic table", "A compiler", "A centrifuge"],
     "answer": 0},
    {"q": "Which limitation of clinical trials does RWE help address?",
     "options": ["Trials are too broad", "Trials follow patients forever", "Trials exclude many real patients and stop at approval", "Trials are free"],
     "answer": 2},
    {"q": "'HEOR' in the RWE world is mostly about:",
     "options": ["Hospital equipment ordering", "Proving a treatment's value to payers", "Hardware error reporting", "Human embryo organ research"],
     "answer": 1},
    {"q": "An 'external control arm' built from RWD is used to:",
     "options": ["Replace the patients entirely", "Stand in for a comparison/placebo group where one isn't ethical or feasible", "Delete trial data", "Increase the drug price"],
     "answer": 1},
    {"q": "A typical data-quality challenge with real-world data is:",
     "options": ["It is always complete", "Missing or fragmented records across systems", "It is generated in a perfect lab", "It never needs cleaning"],
     "answer": 1},
    {"q": "Which best describes Excelra's role in this space?",
     "options": ["It manufactures the drugs", "It curates and analyses real-world data into decision-ready evidence", "It runs the hospitals", "It sells insurance"],
     "answer": 1},
]

PASS_MARK = 0.70  # 70% to pass and unlock the certificate
