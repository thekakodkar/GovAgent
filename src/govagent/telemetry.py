import time
import uuid
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class ExecutionSnapshot(BaseModel):
    """
    v0.2.3 Forensic Snapshot: Captures the 'Why' behind every action.
    """
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    agent_role: str
    task_input: str
    
    # Financial & Operational Metrics
    estimated_cost_usd: float = 0.0
    tokens_used: int = 0
    latency_seconds: float = 0.0
    status: str = "initiated" 
    
    # v0.2.3 Governance Metadata
    # Records which guards (fiscal, policy, judiciary) were triggered
    guards_evaluated: List[str] = []
    governance_status: str = "compliant" # compliant, blocked, overridden
    
    # Business ROI Logic
    human_minutes_saved: float = 0.0
    
    # Audit Trail (Reasoning + Evidence)
    reasoning_steps: List[Dict[str, Any]] = []

class TelemetryManager:
    """
    Forensic collector for the 'Chain of Accountability'.
    """
    def __init__(self, output_path: Optional[str] = "logs/audit_trail.jsonl"):
        self.output_path = output_path
        self.current_session: Optional[ExecutionSnapshot] = None
        self._start_time: float = 0.0

    def start_trace(self, agent_role: str, task: str):
        self._start_time = time.perf_counter()
        self.current_session = ExecutionSnapshot(
            agent_role=agent_role,
            task_input=task
        )

    def log_guard_evaluation(self, guard_name: str, result: str, details: Any = None):
        """Records a governance event within the trace."""
        if self.current_session:
            if guard_name not in self.current_session.guards_evaluated:
                self.current_session.guards_evaluated.append(guard_name)
            
            self.log_step(
                thought=f"Governance Check: {guard_name.upper()}",
                action=f"evaluate_guard_{guard_name}",
                result=result
            )

    def log_step(self, thought: str, action: str, result: str):
        """Appends a reasoning step to the audit trail."""
        if self.current_session:
            step = {
                "timestamp": datetime.utcnow().isoformat(),
                "thought": thought,
                "action": action,
                "result": result
            } # <--- Ensure this is a curly brace '}'
            self.current_session.reasoning_steps.append(step)
            
    def finalize(self, status: str, tokens: int = 0):
        """
        Calculates final ROI and persists the audit trail to disk.
        Satisfies EU AI Act Article 12 (Record-Keeping).
        """
        if not self.current_session:
            return None

        # 1. Update Final Metrics
        self.current_session.status = status
        # ... (rest of your finalization logic)

        # 2. Self-Healing Directory Check
        log_dir = Path("logs")
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        # 3. Persist to JSONL
        try:
            with open(log_dir / "audit_trail.jsonl", "a") as f:
                # Assuming current_session has a .json() or dict conversion
                f.write(str(self.current_session) + "\n")
        except Exception as e:
            print(f"⚠️ Telemetry Persistence Failed: {e}")

        return self.current_session

    def _persist_log(self):
        """Writes to a JSONL file for easy ingestion by Splunk/ELK."""
        if self.output_path and self.current_session:
            try:
                with open(self.output_path, 'a') as f:
                    f.write(self.current_session.model_dump_json() + "\n")
            except Exception as e:
                print(f"⚠️ Telemetry Persistence Failed: {e}")