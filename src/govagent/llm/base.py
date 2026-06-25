from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    prompt: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    system_instruction: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None

class LLMResponse(BaseModel):
    text: str
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    raw_usage: Dict[str, int] = Field(default_factory=dict)  # Crucial for Pillar 2 Fiscal Guard
    model_name: str

class BaseLLMClient(ABC):
    """
    Sovereign LLM abstraction layer. Ensures GovAgent evaluates intent 
    and handles local data redaction uniformly regardless of the provider.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Executes raw generation. Guards hook into this lifecycle out-of-band."""
        pass