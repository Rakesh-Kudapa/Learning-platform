"""
llm.py
------
Thin wrapper around a FREE LLM provider for the per-module "Ask a doubt" tutor.

Pick the provider in .env via LLM_PROVIDER = gemini | groq | ollama.
Uses plain `requests` so there is no heavy SDK to install or version-pin.

If no key is configured, ask_tutor() returns a friendly setup message instead
of crashing — so the rest of the app keeps working during development.
"""
import os
import json
import requests
from course_data import MODULE_CONTEXT, MODULE_TITLES

TIMEOUT = 30


def _ui_settings():
    """Load settings entered via the UI (instance/llm_config.json)."""
    try:
        cfg_path = os.path.join(
            os.path.dirname(__file__), "instance", "llm_config.json"
        )
        with open(cfg_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

SYSTEM_PROMPT = (
    "You are a warm, encouraging tutor inside an Excelra e-learning course on "
    "Real-World Data (RWD) and Real-World Evidence (RWE) for complete beginners. "
    "Answer the learner's question simply and briefly (under 120 words), in plain "
    "language, no jargon dumps. Stay grounded in the module context provided. "
    "If the question is off-topic, gently steer back to the course."
)


def _prompt(module_id, question):
    ctx = MODULE_CONTEXT.get(module_id, "")
    title = MODULE_TITLES[module_id] if 0 <= module_id < len(MODULE_TITLES) else "this module"
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"MODULE: {title}\n"
        f"MODULE CONTEXT:\n{ctx}\n\n"
        f"LEARNER'S QUESTION: {question}\n\n"
        f"Your helpful answer:"
    )


def ask_tutor(module_id, question):
    ui = _ui_settings()
    provider = ui.get("llm_provider") or os.getenv("LLM_PROVIDER", "gemini")
    provider = provider.lower().strip()
    ui_key = ui.get("api_key", "")
    prompt = _prompt(module_id, question)
    try:
        if provider == "gemini":
            return _gemini(prompt, ui_key)
        if provider == "groq":
            return _groq(prompt, ui_key)
        if provider == "ollama":
            return _ollama(prompt)
        return f"Unknown LLM_PROVIDER '{provider}'. Use gemini, groq, or ollama."
    except requests.exceptions.RequestException as e:
        return f"The tutor couldn't reach the AI service right now ({e.__class__.__name__}). Please try again."
    except Exception as e:
        return f"Tutor error: {e}"


def _gemini(prompt, ui_key=""):
    key = ui_key or os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        return ("AI tutor isn't set up yet. Add a free Gemini key to your .env file "
                "(GEMINI_API_KEY) — get one at aistudio.google.com/app/apikey.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=body, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _groq(prompt, ui_key=""):
    key = ui_key or os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        return ("AI tutor isn't set up yet. Add a free Groq key to your .env file "
                "(GROQ_API_KEY) — get one at console.groq.com/keys.")
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.4},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def _ollama(prompt):
    base = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    r = requests.post(
        f"{base}/api/chat",
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()
