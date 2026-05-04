# src/govagent/hitl/__init__.py

from .manager import HITLManager, ApprovalRequest, ApprovalStatus
from .adapters import CLIAdapter, HITLAdapter

# This allows: from govagent.hitl import HITLManager
__all__ = [
    "HITLManager", 
    "ApprovalRequest", 
    "ApprovalStatus", 
    "CLIAdapter", 
    "HITLAdapter"
]