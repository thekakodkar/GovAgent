import yaml
from typing import Dict, Any, List
from govagent.registry import registry

class Policy:
    """
    The Legislative Engine: Translates YAML-based SOPs into 
    executable governance constraints.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metadata = config.get("metadata", {})
        self.agent_name = self.metadata.get("agent_name", "UnknownAgent")
        
        # Mapping YAML tools for O(1) lookup during the audit
        self.tool_rules = {t["name"]: t for t in config.get("tools", [])}

        # Governance section extraction
        gov_section = config.get("governance", {})
        
        # v0.2.0 Standardized Attributes
        # These names are the 'Contract' between Policy and the Guard layer
        self.max_spend_usd = gov_section.get("max_session_cost_usd", 10.0)
        self.confidence_threshold = gov_section.get("confidence_threshold", 0.9)
        self.restricted_domains = gov_section.get("restricted_domains", [])
        self.require_human_approval = gov_section.get("require_human_approval", True)

        # Automated Synchronization Audit
        # Bootstrapping fails if Code and Policy are out of alignment
        self.validate_registry()

    @property
    def allowed_tools(self) -> list:
        """Legacy Bridge: Returns a list of tool names permitted by the policy."""
        return list(self.tool_rules.keys())
    
    @classmethod
    def from_yaml(cls, path: str):
        """Loads the enterprise policy (e.g., healthcare_ops_policy.yaml)."""
        # Note: In production, base_path resolution logic from our previous fix 
        # should be applied before calling this method.
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return cls(config)

    def validate_registry(self):
        """
        The v0.2.0 Governance Audit: Ensures the Python code (@tool) 
        complies with the Executive Policy (YAML).
        """
        print(f"📋 Compliance Audit: Aligning code with '{self.agent_name}' policy...")
        
        # Check for Shadow Tools (Code exists but not in YAML)
        registry.validate_against_policy(self.allowed_tools)

        # Deep Risk-Level Validation
        for tool_name, metadata in registry.tools.items():
            if tool_name not in self.tool_rules:
                continue # shadow check already handled by registry call above
            
            yaml_rule = self.tool_rules[tool_name]
            yaml_risk = yaml_rule.get("risk_level", "low")
            code_risk = metadata.get("risk_level", "low")

            # Strict Enforcement: Code risk cannot be 'weaker' than Policy risk
            # This prevents bypassing HITL for high-stakes actions
            risk_hierarchy = {"low": 1, "medium": 2, "high": 3}
            
            if risk_hierarchy.get(code_risk, 0) < risk_hierarchy.get(yaml_risk, 0):
                raise PermissionError(
                    f"🛑 GOVERNANCE VIOLATION: Tool '{tool_name}' is marked {yaml_risk.upper()} RISK in "
                    f"Policy but only '{code_risk.upper()}' in code. Risk downgrade detected."
                )
        
        print("✅ Governance Alignment: Registry and Policy are synchronized.")

    def is_high_risk(self, tool_name: str) -> bool:
        """Determines if an action requires HITL intervention."""
        # Priority 1: Check the YAML Policy
        rule = self.tool_rules.get(tool_name, {})
        if rule.get("requires_hitl") or rule.get("risk_level") == "high":
            return True
        
        # Priority 2: Check the Registry (Fallback for defensive programming)
        reg_metadata = registry.tools.get(tool_name, {})
        if reg_metadata.get("risk_level") == "high":
            return True
            
        return False