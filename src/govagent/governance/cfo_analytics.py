# src/govagent/governance/cfo_analytics.py

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class CostCenterAllocation(BaseModel):
    cost_center_id: str
    gl_account: str
    allocated_spend_usd: float = 0.0
    transaction_count: int = 0
    token_usage_total: int = 0


class CFORiskReport(BaseModel):
    total_realized_spend_usd: float = 0.0
    value_at_risk_prevented_usd: float = 0.0
    burn_rate_anomaly_detected: bool = False
    average_cost_per_work_unit: float = 0.0
    allocations_by_center: Dict[str, CostCenterAllocation] = Field(default_factory=dict)


class CFOAnalyticsEngine:
    """Calculates ROI metrics, capital risk exposure, and ledger allocations."""

    def __init__(
        self,
        high_burn_threshold_per_run: float = 0.50,
        buffer_path: Optional[str] = None,
    ):
        self.burn_threshold = high_burn_threshold_per_run
        if buffer_path:
            self.buffer_path = Path(buffer_path)
        else:
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            self.buffer_path = project_root / "logs" / "audit_buffer.jsonl"

    def load_buffer_records(self) -> List[Dict[str, Any]]:
        records = []
        if self.buffer_path.exists():
            with open(self.buffer_path, "r", encoding="utf-8") as f:
                for line in f:
                    line_str = line.strip()
                    if line_str:
                        records.append(json.loads(line_str))
        return records

    def analyze(self, ledger_records: Optional[List[Dict[str, Any]]] = None) -> CFORiskReport:
        if ledger_records is None:
            ledger_records = self.load_buffer_records()

        report = CFORiskReport()
        total_units = len(ledger_records)

        for tx in ledger_records:
            spend = float(tx.get("recursive_tco_usd", 0.0))
            report.total_realized_spend_usd += spend

            if spend > self.burn_threshold:
                report.burn_rate_anomaly_detected = True

            # Track financial exposure prevented by Stage 2 or human judiciary
            if tx.get("status") in ["BLOCKED", "VETOED"]:
                potential_exposure = float(tx.get("requested_exposure_usd", 0.0))
                report.value_at_risk_prevented_usd += potential_exposure

            # Financial Allocation to Enterprise Cost Centers
            cc_id = tx.get("cost_center") or "CC-GENAI-DEFAULT"
            gl = tx.get("gl_account") or "GL-640100-SOFTWARE"

            if cc_id not in report.allocations_by_center:
                report.allocations_by_center[cc_id] = CostCenterAllocation(
                    cost_center_id=cc_id,
                    gl_account=gl,
                )

            alloc = report.allocations_by_center[cc_id]
            alloc.allocated_spend_usd += spend
            alloc.transaction_count += 1
            alloc.token_usage_total += int(tx.get("total_tokens", 0))

        if total_units > 0:
            report.average_cost_per_work_unit = report.total_realized_spend_usd / total_units

        return report