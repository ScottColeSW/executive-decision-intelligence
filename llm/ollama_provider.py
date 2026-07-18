"""
Ollama Provider
"""

import requests
import yaml


class OllamaProvider:

    def __init__(self):

        with open("config.yaml") as f:

            config = yaml.safe_load(f)

        self.url = config["llm"]["endpoint"] + "/api/generate"

        self.model = config["llm"]["model"]

    def ask(self, prompt):

        try:

            response = requests.post(

                self.url,

                json={

                    "model": self.model,

                    "prompt": prompt,

                    "stream": False

                },

                timeout=120

            )

            response.raise_for_status()

            return response.json()["response"]

        except Exception as ex:

            return f"Ollama unavailable.\n\n{ex}"