import functools
from typing import Dict, Callable, Any, List
from .schemas import ToolManifest

class GlobalRegistry:
    """Institutional Singleton for tool-to-policy mapping."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalRegistry, cls).__new__(cls)
            cls._instance.tools = {}
        return cls._instance

    def register_tool(self, func: Callable, manifest: ToolManifest):
        """Legislates a function into the sovereign manifest."""
        self.tools[manifest.name] = {"func": func, "manifest": manifest}

    def validate_against_policy(self, allowed_tools: List[str]):
        """STAGE 3: Detects 'Shadow IT' during initialization."""
        for tool_name in self.tools.keys():
            if tool_name not in allowed_tools:
                print(f"⚠️ GOVERNANCE ALERT: Unapproved tool '{tool_name}' detected.")
    
    # src/govagent/registry/manager.py
def validate_intent_schema(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """STAGE 4 Verification: Validates intent against institutional standards."""
    if tool_name not in self.tools:
        return {"valid": False, "error": "Tool not legislated"}

    # v0.6.0 Hardening: Ensure financial amounts are actually numeric
    if "amount" in arguments:
        try:
            float(arguments["amount"])
        except (ValueError, TypeError):
            # THIS TRIGGERS THE EXPECTED EXCEPTION IN THE TEST
            raise ValueError(f"Institutional Integrity Failure: 'amount' must be numeric.")

    return {"valid": True, "status": "AUTHORIZED"}

def tool(name: str, description: str = None, guards: List[str] = None, risk_level: str = "low"):
    """
    Sovereign Decorator: Intercepts and registers institutional actions.
    Ensures compliance with Article 14 (Risk Leveling).
    """
    def decorator(func):
        registry_instance = GlobalRegistry()
        manifest = ToolManifest(
            name=name,
            description=description or func.__doc__ or "No description provided",
            parameters={}, # Schema extraction reserved for v0.6.0 expansion
            risk_level=risk_level
        )
        registry_instance.register_tool(func, manifest)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator