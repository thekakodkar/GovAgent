import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class MetaGovernor:
    """
    v0.6.0 Optimization Layer.
    Analyzes systemic friction to propose policy amendments via the 'Self-Healing' loop.
    """
    def __init__(self, log_path: str = "logs/audit_buffer.jsonl"):
        self.log_path = Path(log_path)
        self.friction_threshold = 3 

    def analyze_friction(self) -> Dict[str, Any]:
        """
        Scans the Article 12 ledger for Recursive TCO blocks.
        """
        if not self.log_path.exists():
            return {"status": "OPTIMAL", "reason": "No forensic data available."}

        rejections = []
        try:
            with open(self.log_path, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    # Updated to match the v0.5.1 Status schema
                    if "blocked" in entry.get("status", "").lower() and "fiscal" in entry.get("status", "").lower():
                        rejections.append(entry)
        except Exception as e:
            return {"status": "ERROR", "reason": f"Audit ingestion failure: {str(e)}"}

        if len(rejections) >= self.friction_threshold:
            return self._draft_amendment(rejections)
        
        return {"status": "OPTIMAL", "reason": "Systemic friction within tolerance."}

    def _draft_amendment(self, rejections: List[Dict]) -> Dict[str, Any]:
        """
        Drafts a Legislative Amendment to lift fiscal ceilings.
        """
        # Calculate impact based on the actual requested amounts in the logs
        avg_request = sum(r.get("metrics", {}).get("requested_amount", 0.0) for r in rejections) / len(rejections)
        proposed_limit = max(avg_request * 1.1, 500.0 * 1.2) # Smart Scaling
        
        return {
            "type": "POLICY_AMENDMENT_PROPOSAL",
            "version": "0.6.0-alpha",
            "timestamp": datetime.utcnow().isoformat(),
            "reason": f"Friction detected: {len(rejections)} blocks. Redacting budget bottlenecks.",
            "proposed_limit": round(proposed_limit, 2),
            "affected_policy": rejections[0].get("policy_id", "finance_policy")
        }