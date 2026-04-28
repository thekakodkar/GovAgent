from pydantic import BaseModel, Field
from typing import List, Optional

class Policy(BaseModel):
    """The Governance Manifest schema for enterprise control."""
    version: str = "1.0"
    agent_name: str
    
    # Financial Guardrails
    max_spend_usd: float = Field(default=1.0, description="Hard limit for API costs")
    
    # Action Scopes
    allowed_tools: List[str] = Field(default_factory=list)
    restricted_domains: List[str] = Field(default_factory=list)
    
    # Escalation
    require_human_approval: bool = True
    confidence_threshold: float = 0.85  # Pause if the model is unsure