# src/govagent/registry/manager.py
import functools
import logging
from typing import Dict, Callable, Any, List
from govagent.registry.schemas import ToolManifest
from govagent.registry.harbor_verifier import HarborVerifier
from govagent.guards.circuit_breaker import GovernanceViolation

logger = logging.getLogger("govagent.registry.manager")

class GlobalRegistry:
    """Institutional Singleton for tool-to-policy mapping with OCI supply chain gating."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalRegistry, cls).__new__(cls)
            cls._instance.tools = {}
            cls._instance.harbor = HarborVerifier()
        return cls._instance

    def register_tool(self, func: Callable, manifest: ToolManifest):
        """Legislates a function into the sovereign manifest."""
        self.tools[manifest.name] = {"func": func, "manifest": manifest}

    def verify_and_resolve_tool(self, tool_name: str) -> Callable:
        """STAGE 5: Intercepts tools to run out-of-band Harbor OCI container verification."""
        if tool_name not in self.tools:
            raise GovernanceViolation(f"REGISTRY EXCEPTION: Tool '{tool_name}' is not authorized.")

        tool_data = self.tools[tool_name]
        manifest = tool_data["manifest"]

        # Only enforce Harbor verification if OCI coordinates are declared
        if manifest.oci_repository and manifest.artifact_digest:
            scan_report = self.harbor.verify_tool_artifact(
                repository=manifest.oci_repository,
                artifact_digest=manifest.artifact_digest
            )
            if not scan_report["verified"]:
                raise GovernanceViolation(
                    f"HARBOR REGISTRY BLOCK: Tool failed image validation. Details: {scan_report['details']}"
                )

        logger.info(f"✅ Supply Chain Approved: Tool '{tool_name}' cleared for execution.")
        return tool_data["func"]

    def validate_against_policy(self, allowed_tools: List[str]):
        """STAGE 3: Detects 'Shadow IT' during initialization."""
        for tool_name in self.tools.keys():
            if tool_name not in allowed_tools:
                print(f"⚠️ GOVERNANCE ALERT: Unapproved tool '{tool_name}' detected.")
    
    def validate_intent_schema(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """STAGE 4 Verification: Validates intent against institutional standards."""
        if tool_name not in self.tools:
            return {"valid": False, "error": "Tool not legislated"}

        if "amount" in arguments:
            try:
                float(arguments["amount"])
            except (ValueError, TypeError):
                raise ValueError(f"Institutional Integrity Failure: 'amount' must be numeric.")

        return {"valid": True, "status": "AUTHORIZED"}

def tool(name: str, description: str = None, risk_level: str = "low", oci_repository: str = None, artifact_digest: str = None):
    """Sovereign Decorator: Intercepts and registers institutional actions with OCI scopes."""
    def decorator(func):
        registry_instance = GlobalRegistry()
        manifest = ToolManifest(
            name=name,
            description=description or func.__doc__ or "No description provided",
            parameters={},
            risk_level=risk_level,
            oci_repository=oci_repository,
            artifact_digest=artifact_digest
        )
        registry_instance.register_tool(func, manifest)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator