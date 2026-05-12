# src/govagent/registry/__init__.py
from .manager import GlobalRegistry, tool
from .schemas import ToolManifest, ExecutionSnapshot

# Singleton instance for institutional state persistence
registry = GlobalRegistry()

__all__ = ["registry", "GlobalRegistry", "tool", "ToolManifest", "ExecutionSnapshot"]