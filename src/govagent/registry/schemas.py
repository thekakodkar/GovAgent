from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class ToolManifest(BaseModel):
    """Institutional Metadata for Registry Legislation."""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "low" # Triggers Federated Judiciary if 'high'

class ExecutionSnapshot(BaseModel):
    """Certified Forensic Snapshot for Article 12 Compliance."""
    trace_id: str
    status: str
    output: Any
    metrics: Dict[str, Any] = Field(default_factory=dict) # v0.6.0 Fiscal Data
    parent_trace_id: Optional[str] = None # Inherited in Swarm Delegation