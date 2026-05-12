from typing import Dict, Any, List
from govagent.context import get_shared_fiscal_metrics, update_shared_spend
from .semantic import SemanticGuard
from .privacy import PrivacyGuard

class GovernanceViolation(Exception):
    """Institutional Exception raised on policy breach."""
    pass

class CircuitBreaker:
    """Unified Enforcement Layer (v0.5.0)."""
    def __init__(self, policy, semantic_guard: SemanticGuard):
        self.policy = policy
        self.semantic_guard = semantic_guard
        self.privacy = PrivacyGuard(policy)

    def _get_gov_config(self) -> dict:
        # Safe access to the internal policy manifest
        return getattr(self.policy, 'config', {}).get('governance', {})

    def check_financial_risk(self, total_projected_cost: float):
        """Stage 2: Recursive TCO Enforcement."""
        limits = getattr(self.policy, 'config', {}).get('global_limits', {})
        tco_limit = limits.get("recursive_tco_ceiling", 150.0)
        
        if total_projected_cost > tco_limit:
            raise GovernanceViolation(
                f"RECURSIVE TCO REJECT: Spend ${total_projected_cost} exceeds ceiling ${tco_limit}."
            )

    async def evaluate(self, tool_name: str, args: Dict[str, Any], thought: str = ""):
        """v0.5.0 Standard: Three-Stage Sovereignty Check."""
        gov = self._get_gov_config()
        
        # STAGE 1: Semantic Alignment
        if thought:
            semantic_cfg = gov.get("semantic_alignment", {})
            min_score = semantic_cfg.get("min_similarity_score", 0.85)
            score = self.semantic_guard.evaluate_alignment(thought)
            if score < min_score:
                raise GovernanceViolation(f"SEMANTIC REJECT: Alignment {score} below threshold {min_score}.")

        # STAGE 2: Fiscal Check
        projected = args.get("amount", 0.0)
        self.check_financial_risk(get_shared_fiscal_metrics()["cumulative_spend"] + projected)

        # STAGE 3: Policy Check
        restricted = gov.get("restricted_domains", [])
        for value in args.values():
            if any(domain in str(value) for domain in restricted):
                raise GovernanceViolation(f"POLICY REJECT: Restricted domain '{value}' denied.")
        return True