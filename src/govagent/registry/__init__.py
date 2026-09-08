# src/govagent/registry/__init__.py
from typing import Dict, Any, Optional, Callable, List
from pydantic import BaseModel, ValidationError, ConfigDict

from .schemas import (
    ExecutionSnapshot,
    ToolManifest,
    FinancialTransactionIntent,
)


class GlobalRegistry:
    def __init__(self):
        self._tools: Dict[str, Any] = {}

    @property
    def tools(self) -> Dict[str, Any]:
        """Public accessor for registered tools mapping."""
        return self._tools

    def register_tool(self, name: str, func: Any, schema: Optional[type[BaseModel]] = None, **kwargs):
        manifest_data = {
            "func": func,
            "schema": schema,
            "risk_level": kwargs.get("risk_level", "low"),
            "cost_usd": kwargs.get("cost_usd", 0.0),
        }
        self._tools[name] = manifest_data

    def get_tool(self, name: str):
        return self._tools.get(name)

    def validate_against_policy(self, allowed_tools: List[str]) -> bool:
        """Audits all registered runtime tools against policy-approved tool manifests."""
        for tool_name in self._tools.keys():
            if allowed_tools and tool_name not in allowed_tools:
                raise PermissionError(f"🛑 UNAUTHORIZED TOOL DETECTED: '{tool_name}' violates policy boundary.")
        return True

    def validate_intent_schema(self, action: str, params: Dict[str, Any]) -> bool:
        """Validates parameters against registered schemas or standard financial intent models."""
        tool_entry = self.get_tool(action)
        schema_cls = None

        if tool_entry and tool_entry.get("schema"):
            schema_cls = tool_entry["schema"]
        elif action == "execute_financial_transaction":
            schema_cls = FinancialTransactionIntent

        if schema_cls:
            schema_cls.model_validate(params)

        return True


# Global registry singleton
registry = GlobalRegistry()


def tool(name: Optional[str] = None, schema: Optional[type[BaseModel]] = None, **kwargs):
    """Decorator to register functions into the govAgent GlobalRegistry."""
    def decorator(func: Callable):
        tool_name = name or func.__name__
        registry.register_tool(name=tool_name, func=func, schema=schema, **kwargs)
        return func
    return decorator


__all__ = [
    "registry",
    "tool",
    "GlobalRegistry",
    "ExecutionSnapshot",
    "ToolManifest",
    "FinancialTransactionIntent",
]