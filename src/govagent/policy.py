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

        # FIX: Explicitly set the attributes the Agent looks for
        # Ensure these names match what the ExecutiveAgent/Guards call
        gov_section = config.get("governance", {})
        
        # Governance Constants
        self.max_spend_usd = gov_section.get("max_session_cost_usd", 10.0)
        self.confidence_threshold = config.get("governance", {}).get("confidence_threshold", 0.9)
    
        # NEW: Domain Restricted List (Required for v0.1.5/v0.2.0 Guardrails)
        # Initialize as empty list if not present in YAML
        self.restricted_domains = gov_section.get("restricted_domains", [])
        
    @property
    def allowed_tools(self) -> list:
        """
        Legacy Bridge: Returns a list of tool names permitted by the policy.
        Required by ExecutiveAgent's Guard layer.
        """
        return list(self.tool_rules.keys())
    
    @classmethod
    def from_yaml(cls, path: str):
        """Loads the enterprise policy (e.g., healthcare_ops_policy.yaml)."""
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return cls(config)

    def validate_registry(self):
        """
        The v0.2.0 Governance Audit: Ensures the Python code (@tool) 
        complies with the Executive Policy (YAML).
        """
        print(f"📋 Compliance Audit: Aligning code with '{self.agent_name}' policy...")
        
        for tool_name, metadata in registry.tools.items():
            # 1. Verification: Does the tool exist in the Policy?
            if tool_name not in self.tool_rules:
                print(f"⚠️  Shadow Tool Detected: '{tool_name}' is not defined in the YAML policy.")
                continue
            
            yaml_rule = self.tool_rules[tool_name]
            yaml_risk = yaml_rule.get("risk_level")
            code_risk = metadata.get("risk_level")

            # 2. Strict Enforcement: Code risk cannot be lower than Policy risk
            # This prevents bypassing HITL for high-stakes actions
            if yaml_risk == "high" and code_risk != "high":
                raise PermissionError(
                    f"GOVERNANCE VIOLATION: Tool '{tool_name}' is marked HIGH RISK in "
                    f"Policy but only '{code_risk}' in code. Execution blocked."
                )
        
        print("✅ Governance Alignment: Registry and Policy are synchronized.")

    def is_high_risk(self, tool_name: str) -> bool:
        """
        Determines if an action requires HITL intervention based on 
        the YAML rule or the registry metadata.
        """
        # Priority 1: Check the YAML Policy
        rule = self.tool_rules.get(tool_name, {})
        if rule.get("requires_hitl") or rule.get("risk_level") == "high":
            return True
        
        # Priority 2: Check the Registry (Fallback)
        reg_metadata = registry.tools.get(tool_name, {})
        if reg_metadata.get("risk_level") == "high":
            return True
            
        return False

    def get_allowed_tools(self) -> List[str]:
        """Returns a list of names for all tools permitted by the YAML."""
        return list(self.tool_rules.keys())