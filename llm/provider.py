from abc import ABC, abstractmethod
from typing import Dict, Any, Generator

class BaseLLMProvider(ABC):
    """Abstract Base Class defining the operational contract for all LLM connectors."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model_name")

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Execute a synchronous text generation request."""
        pass

    @abstractmethod
    def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Generator[str, None, None]:
        """Execute a streaming text generation request."""
        pass