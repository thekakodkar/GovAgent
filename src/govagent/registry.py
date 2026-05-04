import functools
import inspect
from typing import Any, Callable, Dict, Optional

class ToolRegistry:
    """
    The Legislative Registry: Acts as a central repository for governed tools.
    Enables metadata binding (risk levels) directly to Python functions.
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def tool(
        self, 
        name: Optional[str] = None, 
        risk_level: str = "low", 
        category: str = "general"
    ):
        def decorator(func: Callable):
            tool_name = name or func.__name__
            description = func.__doc__.strip() if func.__doc__ else "No description."

            # v0.2.0 Enhanced Metadata: Includes signature for interface validation
            self.tools[tool_name] = {
                "func": func,
                "name": tool_name,
                "risk_level": risk_level,
                "category": category,
                "description": description,
                "signature": str(inspect.signature(func))
            }

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            
            wrapper._is_gov_tool = True
            wrapper._tool_metadata = self.tools[tool_name]
            return wrapper
        
        return decorator

    # --- v0.2.0 NEW: Audit & Synchronization Methods ---

    def get_tool_list(self) -> list:
        """Standardized tool manifest for LLM System Prompting."""
        return [
            {"name": k, "description": v["description"]} 
            for k, v in self.tools.items()
        ]

    def validate_against_policy(self, allowed_tools: list):
        """
        The v0.2.0 'Sanity Check'. 
        Ensures no 'Shadow Tools' exist in code that aren't in the YAML.
        """
        code_tools = set(self.tools.keys())
        policy_tools = set(allowed_tools)
        
        unauthorized = code_tools - policy_tools
        
        if unauthorized:
            raise ImportError(
                f"🛑 Governance Violation: The following tools are defined in code "
                f"but NOT authorized in the Policy YAML: {unauthorized}"
            )
        
        return True

# Global Registry Instance (The Singleton)
registry = ToolRegistry()
tool = registry.tool