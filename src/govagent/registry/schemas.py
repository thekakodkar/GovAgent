# src/govagent/registry/schemas.py

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


class FinancialTransactionIntent(BaseModel):
    """Strict schema for financial execution tools."""
    amount: float
    model_config = ConfigDict(extra="forbid", strict=True)

    @field_validator("amount", mode="before")
    def validate_numeric_amount(cls, v):
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                raise ValueError(f"Invalid monetary value: '{v}' is not a valid float.")
        if not isinstance(v, (int, float)):
            raise TypeError("Amount must be an integer or float.")
        return float(v)


class ToolManifest(BaseModel):
    """Metadata and validation schema for registered tools."""
    name: str
    description: str
    risk_level: str = "LOW"
    cost_usd: float = 0.0
    requires_approval: bool = False
    param_schema: Optional[type[BaseModel]] = None
    oci_repository: Optional[str] = None
    artifact_digest: Optional[str] = None


class ExecutionSnapshot(BaseModel):
    """Certified Forensic Snapshot for Article 12 Compliance."""
    trace_id: str
    status: str
    output: Any = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    parent_trace_id: Optional[str] = None

    timestamp: Optional[str] = None
    selected_model: Optional[str] = "undefined"
    recursive_tco_usd: float = 0.0
    reasoning_steps: List[str] = Field(default_factory=list)
    guards_evaluated: List[str] = Field(default_factory=list)
    block_reason: Optional[str] = None
    tool_hashes: List[str] = Field(default_factory=list)
    judiciary_record: Optional[Dict[str, Any]] = None

    # Phase 1 Accounting Tags
    cost_center: Optional[str] = "CC-GENAI-DEFAULT"
    gl_account: Optional[str] = "GL-640100-SOFTWARE"
    requested_exposure_usd: Optional[float] = 0.0
    total_tokens: Optional[int] = 0