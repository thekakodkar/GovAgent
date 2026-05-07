# src/govagent/hitl/__init__.py

from .manager import HITLManager, ApprovalRequest, ApprovalStatus
from .adapters import CLIAdapter, HITLAdapter
from .slack_adapter import SlackJudiciaryAdapter

# This allows: from govagent.hitl import HITLManager
__all__ = [
    "HITLManager", 
    "SlackJudiciaryAdapter",
    "ApprovalRequest", 
    "ApprovalStatus", 
    "CLIAdapter", 
    "HITLAdapter"
]
