import functools
import inspect
from typing import Any, Callable, Dict, Optional, List

class ToolRegistry:
    """
    The Legislative Registry v0.3.0: The Institutional Gatekeeper.
    Now supports Automated Interception to decouple business logic from governance.
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def tool(
        self, 
        name: Optional[str] = None, 
        risk_level: str = "low", 
        category: str = "general",
        guards: Optional[List[str]] = None 
    ):
        def decorator(func: Callable):
            tool_name = name or func.__name__
            description = func.__doc__.strip() if func.__doc__ else "No description."

            # v0.3.0: Institutional Guard Mapping
            active_guards = guards or (["fiscal", "policy", "judiciary"] if risk_level == "high" else ["policy"])

            self.tools[tool_name] = {
                "func": func,
                "name": tool_name,
                "risk_level": risk_level,
                "category": category,
                "description": description,
                "guards": active_guards,
                "signature": str(inspect.signature(func))
            }

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                """
                The Automated Interceptor: 
                Physically gates tool execution by locating the active ExecutiveAgent.
                """
                # 1. Locate the active agent context (Institutional Scaling)
                from govagent.context import get_current_agent
                agent = get_current_agent()

                if agent:
                    # 2. Extract value for Fiscal Guard (usually the first float/int param)
                    # This replaces manual 'value' passing in v0.2.3
                    amount = kwargs.get("amount") or (args[0] if args and isinstance(args[0], (int, float)) else 0.0)
                    
                    # 3. AUTOMATED EVALUATION
                    # The dev no longer writes this line. The framework enforces it.
                    await agent.evaluate(
                        guards=active_guards,
                        intent={"action": tool_name, "params": kwargs},
                        value=float(amount)
                    )

                # 4. Business logic executes ONLY if evaluation succeeds
                return await func(*args, **kwargs)
            
            wrapper._is_gov_tool = True
            wrapper._tool_metadata = self.tools[tool_name]
            return wrapper
        
        return decorator

    def get_guards_for_tool(self, tool_name: str) -> List[str]:
        return self.tools.get(tool_name, {}).get("guards", ["policy"])

    def validate_against_policy(self, allowed_tools: List[str]):
        """Ensures 'Shadow IT' tools cannot boot within the framework."""
        code_tools = set(self.tools.keys())
        policy_tools = set(allowed_tools)
        
        unauthorized = code_tools - policy_tools
        if unauthorized:
            raise ImportError(
                f"🛑 Governance Violation: Tool Registry contains unauthorized tools: {unauthorized}. "
                "Update your policy.yaml to authorize these capabilities."
            )
        return True

# Global Registry Instance
registry = ToolRegistry()
tool = registry.tool