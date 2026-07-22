import os
import json
import requests
from pathlib import Path

# Configurable via environment so the same image works bare-metal (default
# localhost) or in Docker, where "localhost" would otherwise resolve to the
# container itself instead of a host-installed Ollama.
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")

# Path to the newly decoupled prompts configuration file
PROMPTS_CONFIG_PATH = Path("data") / "prompts_config.json"

def load_prompts_config() -> dict:
    """Loads prompt definitions and fallback responses from our JSON storage safely."""
    if not PROMPTS_CONFIG_PATH.exists():
        return {}
    try:
        with open(PROMPTS_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def ask_ollama(prompt: str) -> str:
    """
    Queries local Ollama using the llama3.2:latest model.
    Falls back to decoupled structured mock responses in the JSON file if offline.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=8)
        if response.status_code == 200:
            result_json = response.json()
            return result_json.get("response", "No response content generated.")
    except Exception:
        pass

    # --- OFFLINE SIMULATION FALLBACKS (Loaded from decoupled JSON) ---
    config = load_prompts_config()
    fallbacks = config.get("offline_fallbacks", {})
    
    # Identify target scenario key based on matching keywords in the active prompt
    target_key = "default"
    if "SME-CAPEX-001" in prompt or "Hydro-Jetter" in prompt:
        target_key = "SME-CAPEX-001"
    elif "SME-SUNK-002" in prompt or "E-Commerce" in prompt:
        target_key = "SME-SUNK-002"
    elif "SME-AI-003" in prompt or "Review Booster" in prompt:
        target_key = "SME-AI-003"

    case_fallbacks = fallbacks.get(target_key, fallbacks.get("default", {}))

    # Determine if we should return the focus group transcript or the standard executive summary
    if "focus group" in prompt.lower() or "debate" in prompt.lower():
        return case_fallbacks.get("focus_group", "No focus group simulation matches.")
    
    return case_fallbacks.get("executive_report", "No executive report matches.")