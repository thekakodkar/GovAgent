import json
from pathlib import Path
from typing import Dict, List, Any

class MetaGovernor:
    """
    v0.6.0 Optimization Layer.
    Analyzes systemic friction to propose policy amendments.
    """
    def __init__(self, log_path: str = "logs/audit_buffer.jsonl"):
        self.log_path = Path(log_path)
        self.friction_threshold = 3 # Number of rejections before proposing a lift

    def analyze_friction(self) -> Dict[str, Any]:
        """
        Scans the Article 12 ledger for Recursive TCO blocks.
        """
        if not self.log_path.exists():
            return {"status": "OPTIMAL", "reason": "No forensic data available."}

        rejections = []
        with open(self.log_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("status") == "RECURSIVE_TCO_REJECT":
                    rejections.append(entry)

        if len(rejections) >= self.friction_threshold:
            return self._draft_amendment(rejections)
        
        return {"status": "OPTIMAL", "reason": "Friction levels within tolerance."}

    def _draft_amendment(self, rejections: List[Dict]) -> Dict[str, Any]:
        """
        Drafts a Legislative Amendment to lift fiscal ceilings.
        """
        current_limit = rejections[0].get("limit", 500.0)
        proposed_limit = current_limit * 1.20 # Propose 20% lift
        
        return {
            "type": "POLICY_AMENDMENT_PROPOSAL",
            "reason": f"Systemic friction detected: {len(rejections)} TCO rejections.",
            "proposed_limit": proposed_limit,
            "impact": "Reduces operational blockage for complex swarms."
        }