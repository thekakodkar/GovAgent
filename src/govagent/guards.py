from typing import Any, Dict, List
from govagent.policy import Policy

class GovernanceViolation(Exception):
    """Custom exception for audit-ready error handling."""
    pass

class CircuitBreaker:
    """
    Real-time enforcement of the Governance Manifest.
    Provides parameterized circuit breakers for cascading triage.
    """
    def __init__(self, policy: Policy):
        self.policy = policy

    def check_financial_risk(self, value: float, current_session_spend: float = 0.0):
        """
        STAGE 1: Fiscal Circuit Breaker.
        Evaluates transaction value and session totals against policy ceilings.
        """
        # Tool-specific ceiling check
        if value > self.policy.global_limits.get("max_per_transaction", 2000.0):
            raise GovernanceViolation(
                f"FISCAL REJECT: Transaction value ${value} exceeds per-action ceiling."
            )

        # Global budget check
        total_projected = current_session_spend + value
        if total_projected > self.policy.global_limits.get("daily_budget_usd", 100.0):
            raise GovernanceViolation(
                f"FISCAL REJECT: Total spend ${total_projected} exceeds daily budget."
            )

    def check_operational(self, metrics: Dict[str, Any]):
        """
        STAGE 2: Operational Circuit Breaker.
        Validates technical constraints like token counts or rate limits.
        """
        max_tokens = self.policy.global_limits.get("max_tokens_per_run", 4000)
        current_tokens = metrics.get("tokens", 0)
        
        if current_tokens > max_tokens:
            raise GovernanceViolation(
                f"OPERATIONAL REJECT: Token usage {current_tokens} exceeds limit of {max_tokens}."
            )

    def validate_policy(self, tool_name: str, parameters: Dict[str, Any]):
        """
        STAGE 3: Policy Circuit Breaker.
        Whitelist check and domain-specific parameter scrubbing.
        """
        # 1. Whitelist enforcement
        if tool_name not in self.policy.allowed_tools:
            raise GovernanceViolation(
                f"UNAUTHORIZED: {tool_name} is not present in the allowed manifest."
            )

        # 2. Parameter scrubbing for restricted domains
        restricted = self.policy.restricted_domains
        for domain in restricted:
            if any(domain in str(val) for val in parameters.values()):
                raise GovernanceViolation(
                    f"POLICY VIOLATION: Parameter contains restricted domain '{domain}'"
                )

    def check_risk_level(self, tool_name: str) -> str:
        """
        Determines if an action requires Judiciary (Human) escalation.
        Returns: 'ESCALATE' or 'AUTO_APPROVE'
        """
        if self.policy.is_high_risk(tool_name):
            return "ESCALATE"
        return "AUTO_APPROVE"