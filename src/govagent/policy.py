import yaml
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
    # New: Tools that are allowed but REQUIRE human sign-off
    high_risk_tools: List[str] = Field(default_factory=list) 
    restricted_domains: List[str] = Field(default_factory=list)
    
    # Escalation
    require_human_approval: bool = True
    confidence_threshold: float = 0.85

    def is_high_risk(self, tool_name: str) -> bool:
        """Logic check for the Executive Loop to trigger HITL."""
        return tool_name in self.high_risk_tools

    @classmethod
    def from_yaml(cls, file_path: str):
        """Standardizes the loading of governance policies from YAML files."""
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)