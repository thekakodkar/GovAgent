# src/govagent/__init__.py

from .agent import ExecutiveAgent
from .policy import Policy
from .hitl.manager import HITLManager
from .hitl.slack_adapter import SlackJudiciaryAdapter

__all__ = [
    "ExecutiveAgent",
    "Policy",
    "HITLManager",
    "SlackJudiciaryAdapter"
]