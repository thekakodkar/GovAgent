import functools
import inspect
from typing import Any, Callable, Dict, Optional

class ToolRegistry:
    """
    The Legislative Registry: Acts as a central repository for governed tools.
    Enables metadata binding (risk levels) directly to Python functions.
    """
    def __init__(self):
        # Stores tool metadata: { "tool_name": { "func": ... , "risk_level": ... } }
        self.tools: Dict[str, Dict[str, Any]] = {}

    def tool(
        self, 
        name: Optional[str] = None, 
        risk_level: str = "low", 
        category: str = "general"
    ):
        """
        Decorator to register a function as a governed tool.
        
        Args:
            name: Override for the tool name. Defaults to function name.
            risk_level: 'low', 'medium', or 'high'. Triggers HITL if 'high'.
            category: Domain grouping (e.g., 'financial', 'healthcare').
        """
        def decorator(func: Callable):
            tool_name = name or func.__name__
            
            # Extract docstring for the LLM and Audit trail
            description = func.__doc__.strip() if func.__doc__ else "No description."

            # Register metadata
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
            
            # Attach metadata to the wrapper for runtime reflection
            wrapper._is_gov_tool = True
            wrapper._tool_metadata = self.tools[tool_name]
            return wrapper
        
        return decorator

    def get_tool_list(self) -> list:
        """Returns a list of tools for the LLM's system prompt."""
        return [
            {"name": k, "description": v["description"]} 
            for k, v in self.tools.items()
        ]

# Global Registry Instance (The Singleton)
registry = ToolRegistry()
tool = registry.tool