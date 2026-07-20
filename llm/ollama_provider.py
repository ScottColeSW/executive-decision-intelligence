from typing import Dict, Any, Generator, Optional
import ollama
from llm.provider import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    """
    Concrete implementation of BaseLLMProvider for local inference using Ollama.
    Expects config keys:
      - 'model_name': e.g., 'llama3.1', 'mistral', 'qwen2.5'
      - 'host': Optional custom URL (defaults to http://localhost:11434)
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Fallback to default if no model name is explicitly configured
        if not self.model_name:
            self.model_name = "llama3.1"
            
        # Initialize client with custom host if specified in config.yaml
        host = self.config.get("host")
        self.client = ollama.Client(host=host) if host else ollama.Client()

    def _build_messages(self, prompt: str, system_prompt: Optional[str] = None) -> list:
        """Helper to structure the payload into Ollama's chat format."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Executes a blocking, synchronous chat generation request."""
        messages = self._build_messages(prompt, system_prompt)
        
        # Extract Ollama-specific configuration parameters (e.g., temperature, top_k)
        options = kwargs.get("options", {})
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                options=options
            )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed for model {self.model_name}: {e}")

    def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Generator[str, None, None]:
        """Executes a streaming chat generation request yielding tokens as they arrive."""
        messages = self._build_messages(prompt, system_prompt)
        options = kwargs.get("options", {})
        
        try:
            response_stream = self.client.chat(
                model=self.model_name,
                messages=messages,
                options=options,
                stream=True
            )
            for chunk in response_stream:
                yield chunk["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama streaming failed for model {self.model_name}: {e}")