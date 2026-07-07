# src/govagent/registry/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class ToolManifest(BaseModel):
    """Institutional Metadata for Registry Legislation."""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "low" 
    
    # v3.0.0 Supply Chain Additions (Optional to preserve backward compatibility)
    oci_repository: Optional[str] = None
    artifact_digest: Optional[str] = None

class ExecutionSnapshot(BaseModel):
    """Certified Forensic Snapshot for Article 12 Compliance."""
    trace_id: str
    status: str
    output: Any
    metrics: Dict[str, Any] = Field(default_factory=dict) 
    parent_trace_id: Optional[str] = None