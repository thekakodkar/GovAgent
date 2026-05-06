import functools
import inspect
from typing import Any, Callable, Dict, Optional, List

class ToolRegistry:
    """
    The Legislative Registry v0.2.3: Acts as the central metadata bridge.
    Enables declarative guard mapping directly via Python decorators.
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def tool(
        self, 
        name: Optional[str] = None, 
        risk_level: str = "low", 
        category: str = "general",
        # v0.2.3: Declarative guard requirements
        guards: Optional[List[str]] = None 
    ):
        def decorator(func: Callable):
            tool_name = name or func.__name__
            description = func.__doc__.strip() if func.__doc__ else "No description."

            # v0.2.3: Default guard assignment based on risk if none provided
            active_guards = guards or (["fiscal", "judiciary"] if risk_level == "high" else ["policy"])

            self.tools[tool_name] = {
                "func": func,
                "name": tool_name,
                "risk_level": risk_level,
                "category": category,
                "description": description,
                "guards": active_guards, # Storing the 'Safety Manifest'
                "signature": str(inspect.signature(func))
            }

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            
            wrapper._is_gov_tool = True
            wrapper._tool_metadata = self.tools[tool_name]
            return wrapper
        
        return decorator

    def get_guards_for_tool(self, tool_name: str) -> List[str]:
        """Retrieves the mandated guards for a specific tool."""
        return self.tools.get(tool_name, {}).get("guards", ["policy"])

    def validate_against_policy(self, allowed_tools: list):
        """Ensures no 'Shadow Tools' exist in code."""
        code_tools = set(self.tools.keys())
        policy_tools = set(allowed_tools)
        
        unauthorized = code_tools - policy_tools
        if unauthorized:
            raise ImportError(
                f"🛑 Governance Violation: Unauthorized tools in code: {unauthorized}"
            )
        return True

# Global Registry Instance
registry = ToolRegistry()
tool = registry.tool