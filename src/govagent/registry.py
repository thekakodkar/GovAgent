import functools
import inspect
from typing import Any, Callable, Dict, Optional, List, Type
from pydantic import BaseModel, Field, field_validator, ValidationError

class FinancialTransaction(BaseModel):
    """
    Legislated Schema for Financial Pillar.
    Ensures absolute data integrity before the Judiciary is engaged.
    """
    reference_id: str = Field(..., description="Alpha-numeric reference ID")
    amount: float = Field(..., gt=0, description="Transaction amount in USD")

    @field_validator('amount')
    @classmethod
    def enforce_global_ceiling(cls, v: float) -> float:
        if v > 100000: # $100k Institutional Hard-Stop
            raise ValueError("Institutional Ceiling Breached at Schema Level.")
        return v

class ToolRegistry:
    """
    The Legislative Registry v0.4.0: The Deterministic Gatekeeper.
    Now supports Pydantic Validation to eliminate LLM hallucination in tool calls.
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        # Mapping generic actions to strict schemas
        self.schemas: Dict[str, Type[BaseModel]] = {
            "execute_financial_transaction": FinancialTransaction
        }

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
                from govagent.context import get_current_agent
                agent = get_current_agent()

                if agent:
                    # v0.4.0 Phase 1: SCHEMA VALIDATION
                    # Check if this tool has a legislated Pydantic schema
                    if tool_name in self.schemas:
                        try:
                            # Validate the LLM-provided kwargs against the Pydantic Model
                            validated_data = self.schemas[tool_name](**kwargs)
                            kwargs = validated_data.model_dump()
                        except ValidationError as e:
                            # Fails fast before the Judiciary/Fiscal guards are even pinged
                            from govagent.guards import GovernanceViolation
                            raise GovernanceViolation(f"Schema Integrity Breach: {str(e)}")

                    # Extract value for Fiscal Guard
                    amount = kwargs.get("amount") or (args[0] if args and isinstance(args[0], (int, float)) else 0.0)
                    
                    # AUTOMATED EVALUATION
                    await agent.evaluate(
                        guards=active_guards,
                        intent={"action": tool_name, "params": kwargs},
                        value=float(amount)
                    )

                return await func(*args, **kwargs)
            
            wrapper._is_gov_tool = True
            wrapper._tool_metadata = self.tools[tool_name]
            return wrapper
        
        return decorator

    def validate_intent_schema(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Manual trigger for schema validation during the reasoning loop."""
        if action in self.schemas:
            return self.schemas[action](**params).model_dump()
        return params

    def validate_against_policy(self, allowed_tools: List[str]):
        """Shadow IT detection (Article 9 Compliance)."""
        code_tools = set(self.tools.keys())
        policy_tools = set(allowed_tools)
        unauthorized = code_tools - policy_tools
        if unauthorized:
            raise ImportError(f"🛑 Governance Violation: Unauthorized tools detected: {unauthorized}")
        return True

# Global Registry Instance
registry = ToolRegistry()
tool = registry.tool