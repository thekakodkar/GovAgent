import time
import uuid
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from govagent.context import get_shared_fiscal_metrics, get_current_agent
from govagent.exporters.base import BaseExporter # New Pillar 4 Interface

class ExecutionSnapshot(BaseModel):
    """
    v0.4.0 Institutional Evidence: Captures recursive swarm traceability.
    Satisfies EU AI Act Article 12 (Record-Keeping & Traceability).
    """
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_trace_id: Optional[str] = None 
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    agent_role: str
    task_input: str
    
    # Financial & Operational Metrics (Recursive TCO)
    estimated_cost_usd: float = 0.0 
    recursive_tco_usd: float = 0.0  
    tokens_used: int = 0
    latency_seconds: float = 0.0
    status: str = "initiated" 
    
    # Governance Metadata
    guards_evaluated: List[str] = []
    governance_status: str = "compliant" 
    
    # Audit Trail (Reasoning + Evidence)
    reasoning_steps: List[Dict[str, Any]] = []

class TelemetryManager:
    """
    Forensic collector for the 'Chain of Accountability'.
    v0.4.0: Updated to support Cloud-Native Exporters (AWS/Azure/OTEL).
    """
    def __init__(self, output_path: str = "logs/audit_trail.jsonl"):
        self.output_path = output_path
        self.current_session: Optional[ExecutionSnapshot] = None
        self._start_time: float = 0.0
        # Register institutional exporters for cloud-native sinks
        self.exporters: List[BaseExporter] = []

    def add_exporter(self, exporter: BaseExporter):
        """Enroll a new Cloud Sink into the governance chain."""
        self.exporters.append(exporter)

    def start_trace(self, agent_role: str, task: str):
        """Initializes a forensic trace with parent-child linkage."""
        self._start_time = time.perf_counter()
        
        parent_id = None
        active_agent = get_current_agent()
        if active_agent and active_agent.telemetry.current_session:
            parent_id = active_agent.telemetry.current_session.trace_id

        self.current_session = ExecutionSnapshot(
            agent_role=agent_role,
            task_input=task,
            parent_trace_id=parent_id
        )

    def log_guard_evaluation(self, guard_name: str, result: str, details: Any = None):
        """Records a governance event within the trace."""
        if self.current_session:
            if guard_name not in self.current_session.guards_evaluated:
                self.current_session.guards_evaluated.append(guard_name)
            
            self.log_step(
                thought=f"Governance Check: {guard_name.upper()}",
                action=f"evaluate_guard_{guard_name}",
                result=f"{result} | Details: {details}" if details else result
            )

    def log_step(self, thought: str, action: str, result: str):
        """Appends a reasoning step to the audit trail."""
        if self.current_session:
            step = {
                "timestamp": datetime.utcnow().isoformat(),
                "thought": thought,
                "action": action,
                "result": result
            }
            self.current_session.reasoning_steps.append(step)
            
    async def finalize(self, status: str, tokens: int = 0, cost: float = 0.0):
        """
        Finalizes ROI and dispatches to all registered Cloud Sinks.
        Ensures penny-accurate TCO is synced across the recursive swarm.
        """
        if not self.current_session:
            return None

        # 1. Update Metrics
        self.current_session.status = status
        self.current_session.tokens_used = tokens
        self.current_session.estimated_cost_usd = cost
        self.current_session.latency_seconds = time.perf_counter() - self._start_time

        # 2. Sync Shared Fiscal Metrics (Recursive TCO)
        metrics = get_shared_fiscal_metrics()
        self.current_session.recursive_tco_usd = metrics["cumulative_spend"]

        # 3. Local Persistence (Primary Evidence)
        snapshot_dict = self.current_session.model_dump()
        self._persist_log()

        # 4. Cloud Dispatch (Institutional Sovereignty)
        # Streams the snapshot to AWS/Azure/OTEL endpoints asynchronously
        for exporter in self.exporters:
            try:
                await exporter.export(snapshot_dict)
            except Exception as e:
                print(f"⚠️ Cloud Export Dispatch Failed: {e}")

        return self.current_session

    def _persist_log(self) -> Optional[ExecutionSnapshot]:
        """Writes to a JSONL file for easy ingestion by Splunk/ELK."""
        if not self.current_session:
            return None

        log_path = Path(self.output_path)
        if not log_path.parent.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(log_path, 'a') as f:
                f.write(self.current_session.model_dump_json() + "\n")
        except Exception as e:
            print(f"⚠️ Telemetry Persistence Failed: {e}")

        return self.current_session