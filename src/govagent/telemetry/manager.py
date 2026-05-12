import json, os, uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ExecutionSnapshot(BaseModel):
    """Forensic Data Model with Article 12 Traceability."""
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_trace_id: Optional[str] = None
    agent_id: str
    task_input: str
    status: str = "pending"
    estimated_cost_usd: float = 0.0
    recursive_tco_usd: float = 0.0
    guards_evaluated: List[str] = Field(default_factory=list)
    steps: List[Dict] = Field(default_factory=list)

class TelemetryManager:
    """Forensic Evidence Engine with Self-Healing DLQ and Swarm Traceability."""
    def __init__(self, buffer_path: str = "logs/audit_buffer.jsonl"):
        self.exporters = []
        self.current_session: Optional[ExecutionSnapshot] = None
        self.buffer_path = buffer_path
        os.makedirs(os.path.dirname(self.buffer_path), exist_ok=True)

    def add_exporter(self, exporter: Any):
        """Restores the Cloud SOC sink registration capability."""
        self.exporters.append(exporter)

    def start_trace(self, agent_id: str, task: str, parent_id: Optional[str] = None):
        """
        Initiates a forensic record. 
        Auto-inherits parent context if present to satisfy Article 12.
        """
        from govagent.context import get_shared_fiscal_metrics, get_current_agent
        
        # 1. RESOLVE PARENT TRACE ID (The Swarm Handshake)
        # If no explicit ID is passed, check the institutional context for an active parent.
        if not parent_id:
            parent_agent = get_current_agent()
            if parent_agent and parent_agent.telemetry.current_session:
                parent_id = parent_agent.telemetry.current_session.trace_id

        self.current_session = ExecutionSnapshot(
            agent_id=agent_id, 
            task_input=task, 
            parent_trace_id=parent_id,
            recursive_tco_usd=get_shared_fiscal_metrics().get("cumulative_spend", 0.0)
        )
        return self.current_session.trace_id

    def log_step(self, thought: str, action: str, result: str):
        if self.current_session:
            self.current_session.steps.append({"thought": thought, "action": action, "result": result})

    async def finalize(self, status: str = "success", tokens: int = 0):
        if not self.current_session: return
        self.current_session.status = status
        
        snapshot = self.current_session.model_dump()
        for exporter in self.exporters:
            try:
                await exporter.export(snapshot)
            except Exception as e:
                self._buffer_to_dlq(snapshot, str(e))
        return self.current_session

    def _buffer_to_dlq(self, snapshot: dict, error: str):
        snapshot["governance_error"] = error
        with open(self.buffer_path, "a") as f:
            f.write(json.dumps(snapshot) + "\n")