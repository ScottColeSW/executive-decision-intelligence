"""
EDI Local Ollama Client

Connects Executive Decision Intelligence
to a local Ollama instance.
"""

import requests
import yaml


CONFIG_FILE = "config.yaml"


def load_config():

    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)


config = load_config()

OLLAMA_HOST = config["llm"]["host"]

OLLAMA_URL = (
    f"{OLLAMA_HOST}/api/generate"
)

MODEL = config["llm"]["model"]


def ask_ollama(prompt: str) -> str:
    """
    Sends a prompt to local Ollama.
    """

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "No response returned from Ollama."
        )


    except requests.exceptions.ConnectionError:

        return (
            "EDI Analyst unavailable.\n\n"
            "Ollama is not running.\n"
            "Running deterministic analysis only."
        )


    except Exception as e:

        return (
            "EDI Analyst encountered an error:\n\n"
            f"{str(e)}"
        )