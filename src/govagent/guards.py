from typing import Any, Dict
from govagent.policy import Policy
from govagent.telemetry import ExecutionSnapshot

class GovernanceViolation(Exception):
    """Custom exception for audit-ready error handling."""
    pass

class CircuitBreaker:
    """
    Real-time enforcement of the Governance Manifest.
    """
    def __init__(self, policy: Policy):
        self.policy = policy

    def check_financial_risk(self, current_spend: float):
        """Prevents further execution if budget is exceeded."""
        if current_spend >= self.policy.max_spend_usd:
            raise GovernanceViolation(
                f"Budget Exceeded: Current spend ${current_spend:.4f} "
                f"exceeds limit of ${self.policy.max_spend_usd}"
            )

    def validate_action(self, tool_name: str, parameters: Dict[str, Any]):
        """
        Validates the intended action against the whitelist 
        and inspects for restricted domains.
        """
        # Whitelist check
        if tool_name not in self.policy.allowed_tools:
            raise GovernanceViolation(f"Unauthorized Tool: {tool_name} is not in the allowed manifest.")

        # Restricted domain check (e.g., blocking specific URLs or IPs)
        for domain in self.policy.restricted_domains:
            if any(domain in str(val) for val in parameters.values()):
                raise GovernanceViolation(f"Access Denied: Parameter contains restricted domain '{domain}'")

    def assess_confidence(self, score: float):
        """Forces Human-in-the-Loop if AI confidence is low."""
        if score < self.policy.confidence_threshold:
            # In a production loop, this would trigger the HITL protocol
            return "ESCALATE_TO_HUMAN"
        return "PROCEED"