from typing import Any, Dict, List
from govagent.policy import Policy
from presidio_analyzer import AnalyzerEngine,PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from govagent.context import get_shared_fiscal_metrics # Integrated Phase 2 logic

class PrivacyGuard:
    """Stage 0 Defense: Pre-LLM PII Redaction (Article 9 Compliance)."""
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # NEW: Institutional Address Recognizer (Regex-based backup)
        # Catches standard address formats that NLP might miss
        address_pattern = Pattern(name="address_pattern", regex=r"\d+\s+[A-Z][a-z]+\s+(St|Ave|Rd|Blvd|Lane|Way)", score=0.5)
        address_recognizer = PatternRecognizer(supported_entity="LOCATION", patterns=[address_pattern])
        self.analyzer.registry.add_recognizer(address_recognizer)
        
        # Define core entities to scrub
        self.entities = ["PERSON", "LOCATION", "EMAIL_ADDRESS", "PHONE_NUMBER"]

    def redact_task(self, task: str) -> str:
        """Analyze and redact PII with forced entity checks."""
        # Explicitly pass the entities list to ensure LOCATION is not ignored
        results = self.analyzer.analyze(
            text=task, 
            language='en', 
            entities=self.entities
        )
        
        anonymized = self.anonymizer.anonymize(
            text=task,
            analyzer_results=results
        )
        return anonymized.text
class GovernanceViolation(Exception):
    """Custom exception for audit-ready error handling."""
    pass

class CircuitBreaker:
    """
    Real-time enforcement of the Governance Manifest.
    v0.4.0: Supports Recursive TCO and Distributed Swarm Governance.
    """
    def __init__(self, policy: Policy):
        self.policy = policy
        self.privacy = PrivacyGuard()

    def check_financial_risk(self, value: float):
        """
        STAGE 1: Recursive Fiscal Circuit Breaker.
        Evaluates the aggregate TCO of the entire swarm against master ceilings.
        """
        # 1. Institutional Shared State Query
        fiscal_metrics = get_shared_fiscal_metrics()
        current_swarm_spend = fiscal_metrics["cumulative_spend"]

        # 2. Per-Action Ceiling Check
        action_ceiling = self.policy.global_limits.get("max_per_transaction", 2000.0)
        if value > action_ceiling:
            raise GovernanceViolation(
                f"FISCAL REJECT: Single action value ${value} exceeds per-action ceiling of ${action_ceiling}."
            )

        # 3. Recursive TCO (Total Cost of Operation) Check
        # Prevents 'Budget Fragmentation' across multiple sub-agents
        total_projected = current_swarm_spend + value
        tco_ceiling = self.policy.global_limits.get("daily_budget_usd", 100.0)
        
        if total_projected > tco_ceiling:
            raise GovernanceViolation(
                f"RECURSIVE TCO REJECT: Total swarm spend ${total_projected:.4f} "
                f"would exceed the institutional ceiling of ${tco_ceiling}."
            )

    def check_operational(self, metrics: Dict[str, Any]):
        """
        STAGE 2: Operational Circuit Breaker.
        Validates technical constraints against the Governance Manifest.
        """
        max_tokens = self.policy.global_limits.get("max_tokens_per_run", 4000)
        current_tokens = metrics.get("tokens", 0)
        
        if current_tokens > max_tokens:
            raise GovernanceViolation(
                f"OPERATIONAL REJECT: Token usage {current_tokens} exceeds limit of {max_tokens}."
            )

    def validate_policy(self, tool_name: str, parameters: Dict[str, Any]):
        """
        STAGE 3: Policy Circuit Breaker (The Law).
        Whitelist enforcement and parameter scrubbing.
        """
        # 1. Whitelist enforcement (Shadow IT Detection)
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
        """
        if self.policy.is_high_risk(tool_name):
            return "ESCALATE"
        return "AUTO_APPROVE"